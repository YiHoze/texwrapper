$file = $args[0]
if ( !$file ) { write-output "
xpub.ps1 foo[.tex] -b/-e/-eng -f
 -b: batchmode
 -e: shell-escape
 -eng: texindy
 -f: fully compile
"
return
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

function SetCompileOption ($this) {
  switch ($this) {
    "-e" {
      $modes[1]="-shell-escape"
      $modes[2]="-8bit"
    }
    "-b" {
      $modes[0]="-interaction=batchmode"
    }
    "-f" {
      $modes[0]="-interaction=batchmode"
      $global:fullcompile = $true
    }
    default { SetIndexLanguage($this) }
  }
}

function SetIndexLanguage ($this) {
  Switch ($this) {
  "-eng" {$global:IndexModule = $IndexModules.eng; $global:indexing = $true}
  "-fre" {$global:IndexModule = $IndexModules.fre; $global:indexing = $true}
  "-ger" {$global:IndexModule = $IndexModules.ger; $global:indexing = $true}
  "-ita" {$global:IndexModule = $IndexModules.ita; $global:indexing = $true}
  "-kor" {$global:IndexModule = $IndexModules.kor; $global:indexing = $true}
  "-rus" {$global:IndexModule = $IndexModules.rus; $global:indexing = $true}
  "-spa" {$global:IndexModule = $IndexModules.spa; $global:indexing = $true}
  default {}
  }
}

if ( !(test-path($file)) ) {
  $tex = $file + ".tex"
} else {
  $tex = (get-item $file).basename + ".tex"
}

if (!(test-path($tex))) {write-output "$tex does not exist."; return}

$modes = @("-synctex=1", "", "")
$global:fullcompile = $false
$global:indexing = $false
$global:IndexModule = ''

if ($args[1] -ne $null) { SetCompileOption($args[1]) }
if ($args[2] -ne $null) { SetCompileOption($args[2]) }
if ($args[3] -ne $null) { SetCompileOption($args[3]) }

if ($fullcompile) {
  xelatex $modes $tex
  xelatex $modes $tex
  if ($indexing) {
    $idx = (get-item $tex).basename + ".idx"
    texindy -M $IndexModule $idx
    xelatex $modes $tex
  }  
  xelatex $modes $tex
  texclean.ps1
} else {
  xelatex $modes $tex
  if ($indexing) {
    $idx = (get-item $tex).basename + ".idx"
    texindy -M $IndexModule $idx
  }
}