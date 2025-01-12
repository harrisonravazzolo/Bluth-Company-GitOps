if [[ ! -e /etc/security/audit_control ]] && [[ -e /etc/security/audit_control.example ]];then
    /bin/cp /etc/security/audit_control.example /etc/security/audit_control
  fi

  /bin/launchctl enable system/com.apple.auditd
  /bin/launchctl bootstrap system /System/Library/LaunchDaemons/com.apple.auditd.plist
  /usr/sbin/audit -i
