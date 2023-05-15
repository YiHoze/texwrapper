[CmdletBinding()]
param (
    [alias('f')][string] $fiducial, # 2023-04-06T16:20:00
    [alias('p')][string] $filePattern = '*.xml',
    [alias('o')][string] $output
)

$timeFile = Split-Path -Leaf $PWD
$timeFile = '..\' + $timeFile + '_' + 'zipped_time.txt'

if ([string]::IsNullOrEmpty($fiducial)) {
    if (Test-Path $timeFile) {
        $fiducial = Get-Content $timeFile
        $fiducial = $fiducial.Trim()
    } else {
        Write-Output 'Specify fiducial date and time like "2023-04-06T16:20:00".'
        Exit
    }
}

if ([string]::IsNullOrEmpty($output)) {
    $zipFile = Split-Path -Leaf $PWD
    $today = get-date -format "yyyy-MM-dd"
    $zipFile = $zipFile + '_' + $today + '.zip'
}

if (Test-Path $zipFile) {
    Remove-Item $zipFile
}

$modifiedFiles = @(Get-ChildItem $filePattern -File | Where-Object {$_.LastWriteTime -gt $fiducial} | Select-Object -ExpandProperty Name)

if ($modifiedFiles.Length -gt 0) {
    zip.exe $zipFile $modifiedFiles
    Move-Item -Force $zipFile ..
    $lastZippedTime = get-date -format "yyyy-MM-ddTHH:mm:ss"
    Set-Content -Path $timeFile $lastZippedTime
}