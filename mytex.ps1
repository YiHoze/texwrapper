[CmdletBinding()]
param(
	[string] $file = "mytex.tex",
	[alias("c")][string] $class = "hzguide",
	[alias("h")][switch] $help = $false
)


Function Help
{
write-output "> mytex.ps1 [foo.tex] [-c class]
Available classes: article, hzguide (default), memoir, oblivoir"
}

if ($help) {
	help
	break
}


if ( !($file.EndsWith(".tex")) ) {
	$file = $file + ".tex"
}

if (Test-Path($file)) {
	Write-Output "$file already exsits."
	$answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
	if ($answer -ne 'y') { break }
}
Function ClassArticle
{
$this = "\documentclass{article}
\usepackage{fontspec}
\begin{document}`n
\end{document}" 
return $this
}

Function ClassHzguide 
{
$this = "\documentclass{hzguide}
\LayoutSetup{paper=A4}
\begin{document}`n
\end{document}" 
return $this
}

Function ClassMemoir
{
$this = "\documentclass[a4paper]{memoir} 
\usepackage{fontspec} 
\begin{document}`n
\end{document}"
return $this
}

Function ClassOblivoir 
{
$this = "\documentclass[a4paper]{oblivoir} 
\usepackage{fapapersize}
\usefapapersize{*,*,30mm,*,30mm,*}
\begin{document}`n
\end{document}"
return $this
}

Switch ($class) {
	"article" {$preamble = ClassArticle}
	"hzguide" {$preamble = ClassHzguide}
	"oblivoir" {$preamble = ClassOblivoir}
	"memoir" {$preamble = ClassMemoir}
	default {$preamble = ClassHzguide}
}

Set-Content $file -Encoding UTF8 $preamble
open.ps1 $file