type("Get-WmiObject Win32_OperatingSystem | Format-List * > E:\\SystemProfile.txt\n")
delay(500)
type("Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize > E:\\InstalledApps.txt\n")
delay(500)
type("ipconfig /all > E:\\ForensicData\\NetworkConfig.txt\n")


