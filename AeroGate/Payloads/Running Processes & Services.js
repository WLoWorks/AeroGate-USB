layout('us')
press("GUI r")
delay(500)
type("powershell\n")
delay(1000)
type("Get-Process | Out-File E:\\ForensicData\\RunningProcesses.txt\n")
type("Get-Service | Out-File E:\\ForensicData\\ServicesStatus.txt\n")
type("exit\n")