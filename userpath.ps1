[Cmdletbinding()]
param
(
    [alias("g")][switch] $global_bool = $false,
    [alias("a")][switch] $add_bool = $false,
    [alias("r")][switch] $remove_bool = $false,
    [alias("f")][switch] $refresh_bool = $false,
    [alias("s")][switch] $set_bool = $false,
    [alias("p")][switch] $system_properties_bool = $false,
    [alias("h")][switch] $help_bool = $false,
    [String] $folderPath
)

function help
{
    write-output "
    View the local PATH environment variable.
    Usage:
        userpath.ps1 [option] [directory]
    Options:
        -g: Add to or remove from the global User Path environment variable.
        -a: Add to the path. 
        -r: Remove from the path.
        -f: Refresh the local path.
        -s: Set to the path.
        -p: Open the System Properties window.
        -h: help
    "
}


function GetLocalPath
{
    write-output ""
    $env:path.split(";")
}

function RefreshLocalPath
{
    $systemPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:path = "$systemPath;$userPath"
    GetLocalPath
}
function AddGlobalPath
{
    if (!(TEST-PATH $folderPath)) {
        write-output "'$folderPath' does not exist."
        return
    }
    # 'Machine' for the System variable
    $globalPath = [Environment]::GetEnvironmentVariable('Path', 'User') 
    if ($globalPath.split(';') -icontains $folderPath) {
        write-output "'$folderPath' is already within the global User Path."
    } else {
        $globalPath = "$globalPath;$folderPath"
        $globalPath = $globalPath.Replace(';;', ';')
        [Environment]::SetEnvironmentVariable('PATH', $globalPath, 'User') 
        RefreshLocalPath
    }
}

function AddLocalPath
{
    if (!(TEST-PATH $folderPath)) {
        write-output "'$folderPath' does not exist."
        return
    }
    if ($Env:PATH.split(';') -icontains $folderPath) {
        write-output "'$folderPath' is already within the local Path."
    } else {
        $env:path  =  "$folderPath;$env:path"
        GetLocalPath
    }
}

function RemoveGlobalPath
{
    $globalPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $globalPath = $globalPath.replace($folderPath,$NULL)
    $globalPath = $globalPath.replace(';;',';')
    [Environment]::SetEnvironmentVariable('Path', $globalPath, 'User') 
    RefreshLocalPath
}

function RemoveLocalPath
{
    $env:path = $env:path.replace($folderPath,$NULL)
    $env:path = $env:path.replace(';;',';')
    GetLocalPath
}

function SetLocalPath
{
    $env:path  =  $folderPath
    GetLocalPath
}

if ($help_bool) { help; break }
if ($system_properties_bool) { control.exe sysdm.cpl,System,3; break }
if ($refresh_bool) { RefreshLocalPath; break }
if (! $folderPath) { GetLocalPath; break }
if ($add_bool) { 
    if ($global_bool) {
        AddGlobalPath
    } else {
        AddLocalPath
    }
    break
}
if ($remove_bool) { 
    if ($global_bool) {
        RemoveGlobalPath
    } else {
        RemoveLocalPath
    }
    break
}
if ($set_bool) { SetLocalPath; break }