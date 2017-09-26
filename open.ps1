[CmdletBinding()]
param(
  [string] $file,  
  [alias("c")][switch] $Code=$false,
  [alias("e")][switch] $EmEditor=$false,
  [alias("a")][switch] $Acrobat=$false,
  [alias("s")][switch] $kpsewhich=$false,
  [alias("h")][switch] $help=$false
)

$TextFiles = @(".txt", ".tex", ".sty", ".cls", ".idx", ".ind", ".log", ".bib", ".ipynb", ".md", ".rst", ".css", ".py", ".ps1")

function help {
write-output "
open.ps1 file [option]
 -c: Code
 -e: EmEditor
 -a: Acrobat
 -s: kpsewhich 
 -h: help
"
return
}

function DetermineType($file) 
{
  if ( !(test-path($file)) ) {
    return $false    
  } else {
    $ext = (get-item $file).extension
  }
  if ($ext -eq "pdf") {
    return "pdf"
  } elseif ($TextFiles -contains $ext) {
    return "txt"
  } else {
    return "unknown"
  }
}

function OpenTexmf($file) 
{
  $filepath = kpsewhich $file
  if ($filepath -eq $null) {
    write-output "$file is not found."
    break
  } else {
    OpenTxt($filepath)
  }
}

function OpenTxt($file) {
  if ($EmEditor) {
    emeditor.exe $file
  } else {
    code.cmd $file -r
  }
}

function OpenUnknown($file) 
{
  if ($Code) {
    code.cmd $file -r
  } elseif ($EmEditor) {
    emEditor.exe $file
  } else {
    start $file
  }
}

function OpenPdf($file) 
{
  if ($Acrobat) {
     &"C:\Program Files (x86)\Adobe\Acrobat 10.0\Acrobat\Acrobat.exe" $file
  } else {
     start $file
  }
}

function OpenFile($file) 
{
  $FileType = DetermineType($file)
  if ($FileType) {
    switch ($FileType) {
    "pdf" { OpenPdf($file) }
    "txt" { OpenTxt($file) }
    "unknown" { OpenUnknown($file) }
    }
  } else {
    write-output "$file does not exist."
  }
}

if ( $help -or !$file ) { help; break }

if ($kpsewhich) 
{
  OpenTexmf($file)
} elseif ( $file.contains('*')) {
  foreach ($element in Get-ChildItem $file -name) { OpenFile($element) }
} else {
  OpenFile($file)
}
