# Enable automatic time zone updates
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\tzautoupdate" -Name "Start" -Value 3

# Allow automatic time zone updates
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" -Name "Value" -Value "Allow"

# Restart the time srv
Restart-Service -Name w32time

# Enable automatic time sync
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\w32time\Parameters" -Name "Type" -Value "NTP"

Write-Host "Automatic time settings enabled"

exit 0