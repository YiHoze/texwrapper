$cmd = "dita.bat --input={0} --format=html5 --output=_html --repeat=1" -f $args[0]
Invoke-Expression $cmd
$htmlFile = "{0}.html" -f (Get-Item $args[0]).BaseName
$htmlFile = Join-Path -Path "_html" -ChildPath $htmlFile
# to use the default web browser
# Invoke-Expression $htmlFile
# to use Firefox
&"C:\Program Files\Mozilla Firefox\firefox.exe" (Get-ChildItem $htmlFile).FullName
