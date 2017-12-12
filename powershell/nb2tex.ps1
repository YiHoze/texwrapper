[CmdletBinding()] 
param(
  [string] $name,
  [alias("c")][string] $class="report",
  [alias("o")][switch] $once=$false,
  [alias("f")][switch] $full=$false,
  [alias("h")][switch] $help=$false
)

function help {
write-output "
nb2tex.ps1 notebook_file [options]
  -c: class 
      beamer / report (default)
  -o: compile latex once 
  -f: compile latex fully
  -h: help
"
}

function ConvertToTeX {
  switch ($class) {
  default  {}
  "beamer"  { pandoc -f markdown -t beamer -o $tex --template=$template_path/pd_beamer.txt $md } 
  "report"   { pandoc -f markdown -t latex -o $tex --template=$template_path/pd_report.txt $md } 
  }
}

function CompileTeX {
  switch ($compile) {
    default  { }
    "once"    { xelatex $tex }
    "full"    {
              xelatex $tex
            if ($? -eq $true) {
                xelatex $tex -interaction=batchmode
                #komkindex -s kotex $tex
                #xelatex $tex -interaction=batchmode
                xelatex $tex -interaction=batchmode
            } 
          }
  }
}

if ( !($name) -or $help) { help; break }

if ( $name.endswith(".ipynb") ) {
  $name = (get-childitem $name).basename
} 

$nb = $name + ".ipynb"
$md = $name + ".md"
$tex = $name + ".tex"
$pdf = $name + ".pdf"
$template_path = "d:/home/bin/templates"

if ( !(test-path($nb)) ) { 
  write-output "$nb doesn't exist." 
  break 
} else {
  $compile=''
  if($once) {$compile='once'}
  if($full) {$compile='full'}
  jupyter nbconvert --to=markdown --template=$template_path/nb_markdown.tpl $nb  
  if ($? -eq $true)  { ConvertToTeX }
  if ($? -eq $true)  { CompileTeX }
}