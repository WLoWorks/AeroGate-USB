layout('us')
press("CONTROL ESCAPE") 
delay(500)
type("powershell\n") 
delay(500)
press("CONTROL SHIFT ENTER") 
delay(1000)
press("LEFT") 
press("ENTER")
delay(1000)
type("reg save HKLM\\SAM E:\\ForensicData\\RegistryHives\\SAM.save\n")
delay(500)
type("reg save HKLM\\SYSTEM E:\\ForensicData\\RegistryHives\\SYSTEM.save\n")
delay(500)
type("reg save HKLM\\SECURITY E:\\ForensicData\\RegistryHives\\SECURITY.save\n")




