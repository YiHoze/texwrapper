[CmdletBinding()]
param (
	[string] $No="0"
)

$locations = @(
    "C:\projects\AST",
    "C:\projects\Hanwha\coater\tex\eng",
    "C:\projects\Hanwha\coater\tex\images",
    "C:\projects\private\lua",
    "D:\projects\HMC\_workshop\manual",
	"C:\home\texmf\tex\latex\HzGuide", 
	"C:\home\doc",
	"C:\home\bin",
	"C:\temp"
)

function Show-locations {
	for ($i = 1; $i -le $locations.Count; $i++) {
		Write-Output "$i`t$($locations[$i-1])"
	}
	$question = "Enter a number to go to its folder"
	$answer = Read-Host $question
	try {
		$locationNo = ([int]$answer - 1)
		if ($locationNo -le $locations.Count) {
			Set-Location $locations[$locationNo]
		} else {
			Write-Output "Wrong selection."
			Show-locations
		}
	}
	catch {
		Write-Output "Wrong input."
		Show-locations
	}
}

function set-fromClipboard {
	$clipboard = Get-Clipboard
	if ([System.IO.Path]::IsPathRooted($clipboard)) {
        if (Test-Path $clipboard -PathType Container) {
		    Set-Location $clipboard
        } else { 
            Show-locations
        }
	} else {
		Write-Output "No proper path in the clipboard"
		Show-locations
	}
}

try {
    $locationNo = [int]$No
} catch {
    Show-locations
}

if ($locationNo -eq 0) {
    set-fromClipboard
} elseif ($locationNo -gt 0) {
    $locationNo = $locationNo - 1
    if ($locationNo -le $locations.Count) {
        Set-Location $locations[$locationNo]
    } else {
        Show-locations
    }
} else {
    Show-locations
}
