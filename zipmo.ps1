[CmdletBinding()]
param (
    [alias('f')][string] $fiducial, # 2023-04-06T16:20:00
    [alias('p')][string] $filePattern = '*.*',
    [alias('o')][string] $output
)

if ([string]::IsNullOrEmpty($output)) {
    $fileName = Split-Path -Leaf $PWD
    $today = get-date -format "yyyy-MM-dd"
    $fileName = $fileName + '_' + $today + '.zip'
}

if ([string]::IsNullOrEmpty($fiducial)) {
    if (Test-Path '..\last_zipped_time.txt') {
        $fiducial = Get-Content '..\last_zipped_time.txt'
        $fiducial = $fiducial.Trim()
    } else {
        Write-Output 'Specify fiducial date and time like "2023-04-06T16:20:00".'
        Exit
    }
}

if (Test-Path $fileName) {
    Remove-Item $fileName
}
$modifiedFiles = @(Get-ChildItem $filePattern -File | Where-Object {$_.LastWriteTime -gt $fiducial} | Select-Object -ExpandProperty Name)
zip.exe $fileName $modifiedFiles
if (Test-Path $fileName) {
    Move-Item -Force $fileName ..
}

$lastZippedTime = get-date -format "yyyy-MM-ddTHH:mm:ss"
Set-Content -Path '..\last_zipped_time.txt' $lastZippedTime