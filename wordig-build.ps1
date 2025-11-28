$build = $false
$zip = $false
$upload = $false

if ($args[0] -eq "b") {
    $build = $true
} elseif ($args[0] -eq "z") {
    $zip = $true
} elseif ($args[0] -eq "u") {
    $upload = $true
} 

$today = Get-Date -Format "yyyy-MM-dd"
$installer = "wordig-install_${today}.exe"

if ($build) {
    Remove-Item .\dist\wordig -Recurse -Force -ErrorAction SilentlyContinue
    pyinstaller.exe --onedir --clean --noconfirm wordig.py
}
if ($zip) {
    Remove-Item $installer -ErrorAction SilentlyContinue
    7z.exe a -sfx $installer .\dist\wordig\*
}
if ($upload) {
    pullftp.ps1 wordig $installer -u
}