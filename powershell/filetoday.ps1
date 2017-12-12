[CmdletBinding()]
param(
  [string] $files,
  [alias("d")][string] $date,
  [alias("r")][switch] $remove = $false,  
  [alias("h")][switch] $help = $false
)

function help 
{
write-output "
filetoday.ps1 adds or removes a date from filenames
Usage:
  #>filetoday.ps1 *.foo [options]
Options:
    -d: today date by default (yyyy-mm-dd)
    -r: remove
    -h: help
  "
}

function AppendDate () {
  get-childitem $files | 
  foreach-object { 
    $newname = $_.basename + $date + $_.extension
    rename-item $_.name $newname
  }
}

function RemoveDate () {  
  get-childitem $files |
  foreach-object {
    if ( $_.name.contains($date) ) {
      $oldname = $_.name
      $newname = $oldname.replace($date, "")
      rename-item $_.name $newname
    }    
  }
}

if (!$files) { help; break }

if (!$date) { 
  $date = get-date -format "yyyy-MM-dd"   
}
$date = "_" + $date

if ($remove) { RemoveDate }
else { AppendDate }