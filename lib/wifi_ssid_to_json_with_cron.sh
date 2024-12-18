#!/bin/sh

# Path where the script will be placed
OUTPUT_SCRIPT="/usr/local/bin/wifi_ssid_to_json.sh"
CRON_JOB="0 7 * * * $OUTPUT_SCRIPT"

# Create the Wi-Fi script that outputs to JSON
cat << 'EOF' > "$OUTPUT_SCRIPT"
#!/bin/sh

# Output file for Wi-Fi SSID
OUTPUT_FILE="/tmp/wifi_ssid.json"

# Ensure that nmcli is available
export PATH=$PATH:/usr/bin:/usr/sbin

# Fetch Wi-Fi details using nmcli
wifi_info=$(nmcli -t -f active,ssid dev wifi | grep '^yes')

# Check if there's an active connection
if [ -z "$wifi_info" ]; then
    echo '{"error": "No active Wi-Fi connection found."}' > "$OUTPUT_FILE"
    echo "No active Wi-Fi connection found. JSON written to $OUTPUT_FILE."
    exit 1
fi

# Extract the SSID
ssid=$(echo "$wifi_info" | cut -d: -f2)

# Create JSON output with escaped quotes
json_output=$(cat <<EOF_JSON
{
    "ssid": "$ssid",
    "timestamp": "$(date +"%Y-%m-%dT%H:%M:%S%z")"
}
EOF_JSON
)

# Write JSON to file
echo "$json_output" > "$OUTPUT_FILE"
echo "Wi-Fi SSID information written to $OUTPUT_FILE."
EOF

# Make the newly created script executable
chmod +x "$OUTPUT_SCRIPT"

# Function to check and set up the cron job for root
setup_cron_job() {
    # Check if the cron job is already set for root
    if crontab -l -u root 2>/dev/null | grep -Fq "$OUTPUT_SCRIPT"; then
        echo "Cron job already set up for root."
    else
        # Add the cron job for root
        (crontab -l -u root 2>/dev/null; echo "$CRON_JOB") | crontab -u root -
        echo "Cron job set to run daily at 7:00 AM for root."
    fi
}

# Set up the cron job for root
setup_cron_job
