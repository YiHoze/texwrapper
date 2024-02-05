[CmdletBinding()]
param (
	[string] $fileName="*.md",
    # 무시할 파일 경로
    [Alias("e")][array] $exclusions=@("*\jre\*")
)

$foundFiles = @()

function Open-Found {
    param ( [string]$filePath )

    Set-Clipboard $filePath
    # 디폴트 앱으로 열기
    Start-Process -PassThru -FilePath $filePath  
}

function Confirm-Found {
    if ($foundFiles.Count -eq 0) { 
        Write-Output "No matched files are found."
        return $false
    } else {
        return $true
    }
}

function Limit-Found {
    $filteredFiles = @()

    foreach ($filePath in $foundFiles) {
        $exclude = $false
        foreach ($exclusion in $exclusions) {
            if ($filePath -like $exclusion) {
                $exclude = $true
                break
            }
        }
        if (-not $exclude) {
            $filteredFiles += $filePath
        }
    }
    $foundFiles = $filteredFiles

    return $filteredFiles
}

function Select-Found {
    for ($i = 1; $i -le $foundFiles.Count; $i++) {
        Write-Output "$i`t$($foundFiles[$i - 1])"
    }
    $question = "Enter a number to open its file"
    $answer = Read-Host $question

    try {
        $fileNumber = ([int]$answer - 1)
    } catch {
        Exit
    }

    if (($fileNumber -ge 0) -and ($fileNumber -le $foundFiles.Count)) {
        Open-Found $foundFiles[$fileNumber]
    } 
}

$foundFiles = (Get-ChildItem -Recurse $fileName).FullName
if ( (-not [string]::IsNullOrEmpty($exclusions)) -and ($foundFiles.Count -gt 0)) {
    $foundFiles = Limit-Found
}
if (Confirm-Found) {
    if ($foundFiles.Count -eq 1) { 
        Open-Found $foundFiles
    } else {
        Select-Found
    }
}