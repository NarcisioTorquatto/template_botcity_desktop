$exclude = @("venv", "template_botcity_desktop.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "template_botcity_desktop.zip" -Force