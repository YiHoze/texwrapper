if (!($args[0]) -or ($args[0].StartsWith('-'))) {	
	$file=$args[1]	
	$class = $args[0]
} else {
	$file = $args[0]
	$class = $args[1]
}

if (!($file)) {
	$file="mytex.tex"
} elseif ( !($file.EndsWith(".tex")) ) {
	$file = $file + ".tex"
}

if (Test-Path($file)) {
	Write-Output "$file already exsits."
	$answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
	if (($answer -ne 'y') -or ($answer -ne 'Y')) {
		break
	}
}

Function UseArticle () {
$this = "\documentclass{article}
\usepackage{fontspec}
\begin{document} 

\end{document}" 
return $this
}

Function UseHzguide () {
$this = "\documentclass{hzguide}
\LayoutSetup{paper=A4}
\begin{document} 

\end{document}" 
return $this
}

Function UseMemoir () {
$this = "\documentclass[a4paper]{memoir} 
\usepackage{fontspec} 
\begin{document} 

\end{document}"
return $this
}

Function UseOblivoir () {
$this = "\documentclass[a4paper]{oblivoir} 
\usepackage{fapapersize}
\usefapapersize{*,*,30mm,*,30mm,*}
\begin{document} 

\end{document}"
return $this
}

Switch ($class) {
	"-a" {$preamble = UseArticle}
	"-h" {$preamble = UseHzguide}
	"-o" {$preamble = UseOblivoir}
	"-m" {$preamble = UseMemoir}
	default {$preamble = UseHzguide}
}

Set-Content $file -Encoding UTF8 $preamble
open.ps1 $file