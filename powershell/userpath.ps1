[Cmdletbinding()]
param
(
  [String] $directory,
  [alias("a")][switch] $AppendToPath = $false,
  [alias("r")][switch] $RemoveFromPath = $false,
  [alias("s")][switch] $SetToPath = $false,
  [alias("c")][switch] $IsAdmin = $false,
  [alias("h")][switch] $help = $false
)

function help()
{
  write-output "
  userpath.ps1 manipulates the local path variable.
  Usage:
    userpath.ps1 [directory] [options]
  Options:
    -a: Append to the path
    -r: Remove from the path
    -s: Set to the path
    -c: Check if running as administrator
    -h: help
  "
}

function CheckLocalAdmin()
{
  $result  = ([security.principal.windowsprincipal][security.principal.windowsidentity]::GetCurrent()).isinrole([Security.Principal.WindowsBuiltInRole] "Administrator")
  If ($result) {
    write-output "`n Running as administrator `n"
  } else {
    write-output "`n NOT Running as administrator `n"
  }
}

function GetLocalPath()
{
  write-output ""
  $env:path.split(";")
  write-output ""
}

function AppendLocalPath()
{
  if (!(TEST-PATH $directory)) {
    write-output "'$directory' does not Exist, cannot be added to the path"
    return
  }
  $PathasArray = ($Env:PATH).split(';')
  if ($PathasArray -contains $directory -or $PathAsArray -contains $directory+'\') {
    write-output "'$Directory' already within the path"
    return
  }
  If (!($directory[-1] -match '\\')) {
    $directory  =  $directory + '\'
  }
  $env:path  =  $directory + ";" + $env:path
  GetLocalPath
}

function RemoveLocalPath()
{
  $Verify = $env:path.split(';') -contains $directory
  If ($Verify) {
    $env:path = $env:path.replace($directory,$NULL)
    $env:path = $env:path.replace(';;',';')
  }
  GetLocalPath
}

function SetLocalPath()
{
  $env:path  =  $directory
  GetLocalPath
}

if ($help) { help; break }
if ($IsAdmin) { CheckLocalAdmin; break }
if (! $directory) { GetLocalPath; break }
if ($AppendToPath) { AppendLocalPath; break }
if ($RemoveFromPath) { RemoveLocalPath; break }
if ($SetToPath) { SetLocalPath; break }
