[CmdletBinding()]
param(
  [alias("c")][switch] $Code=$false,
  [alias("e")][switch] $EmEditor=$false,
  [alias("h")][switch] $help=$false
)

$Sumatra = "C:\Program Files\SumatraPDF\SumatraPDF.exe"
#C:\Program Files\EmEditor\emeditor.exe

function help
{
  write-output "
  texeditor.ps1 [option]
  Options:
    -c: Visual Studio Code
    -e: EmEditor
    -h: help
  "
}

function ActivateCode
{
  $env:TEXEDIT = "code.cmd -g %s:%d -r"
  &$Sumatra -inverse-search  "`"C:\Program Files (x86)\Microsoft VS Code\code.exe`" -g %f:%l -r"
}

function ActivateEmeditor
{
    $env:TEXEDIT = "emeditor.exe /l %d %s"
    &$Sumatra -inverse-search "emeditor.exe /l %l %f"
}

if ($help) { help; break }

if ($Code) { ActivateCode }
elseif ($EmEditor) { ActivateEmeditor }
