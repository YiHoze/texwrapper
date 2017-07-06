[CmdletBinding()]
param(
  [string] $file,
  [alias("b")][switch] $batchmode=$false,
  [alias("s")][switch] $shellescape=$false,
  [alias("f")][switch] $fullcompile=$false,
  [alias("i")][string] $lang,
  [alias("h")][switch] $help=$false
)

function help {
write-output "
xlt.ps1 foo.tex [options]
  -b: batchmode
  -s: shell-escape
  -f: compile fully
  -i: language for index sorting
"
}

$IndexModules = @{
  "eng" = "lang/english/utf8-lang";
  "fre" = "lang/french/utf8-lang";
  "ger" = "lang/german/din5007-utf8-lang";
  "ita" = "lang/italian/utf8-lang";
  "kor" = "lang/korean/utf8-lang";
  "rus" = "lang/russian/utf8-lang"
  "spa" = "lang/spanish/modern-utf8-lang";
}

function SetIndexModule ($lang) {
  Switch ($lang) {
  "eng" {return $IndexModules.eng}
  "fre" {return $IndexModules.fre}
  "ger" {return $IndexModules.ger}
  "ita" {return $IndexModules.ita}
  "kor" {return $IndexModules.kor}
  "rus" {return $IndexModules.rus}
  "spa" {return $IndexModules.spa}
  default { return $false }
  }
}

if ( $help -or !$file ) { help; break }

if ( !(test-path($file)) ) {
  $tex = $file + ".tex"
} else {
  $tex = (get-item $file).basename + ".tex"
}
if (!(test-path($tex))) {write-output "$tex does not exist."; break}

$compilemode = New-Object System.Collections.Generic.List[System.Object]

if ($batchmode -or $fullcompile) {
  $compilemode.add("-interaction=batchmode")
} else {
  $compilemode.add("-synctex=1")
}

if ($shellescape) {
  $compilemode.add("-shell-escape")
  $compilemode.add("-8bit")
}

$IndexModule = SetIndexModule($lang)

if ($fullcompile) {
  xelatex $compilemode $tex
  xelatex $compilemode $tex
  if ($IndexModule) {
    $idx = (get-item $tex).basename + ".idx"
    texindy -M $IndexModule $idx
    xelatex $compilemode $tex
  }
  xelatex $compilemode $tex
  texclean.ps1
} else {
  xelatex $compilemode $tex
  if ($IndexModule) {
      $idx = (get-item $tex).basename + ".idx"
      texindy -M $IndexModule $idx
  }
}

if ($fullcompile) {
  $filename = (get-item $tex).basename
  $pdf = $filename + ".pdf"
  $today = get-date -format "yyyy-MM-dd"
  $delivery = $filename + "_" + $today + ".pdf"
  if (Test-Path($delivery)) {
    Write-Output "$delivery already exists."
    $answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
    if ($answer -eq 'y') {
      remove-Item $delivery
      rename-item $pdf $delivery
    } else {
      break
    }
  } else {
    rename-item $pdf $delivery
  }
}
