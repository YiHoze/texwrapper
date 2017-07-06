$font = $args[0]
$file = $args[1]
$num = $args[2]

if (!($font)) { 
Write-Output "fonttypeface.ps1 `"font name`" output-filename [code points]
fonttypeface.ps1 `"Linux Libertine O`" LinuxLibertine(.tex) [FFFF]";
break
}

if (!($num)) {$num="FF"}

if (!($file)) {$file = "typeface.tex"}
if (!($file.EndsWith(".tex"))) {$file = $file + ".tex"}

$tex = "\documentclass[12pt]{hzguide}
	\LayoutSetup{paper=A4}
	\begin{document} 
	\setmainfont{$font}
	\ShowTypeface[$num]
	\end{document}"

Set-Content $file -Encoding UTF8 $tex
xelatex $file
texclean.ps1
Remove-Item($file)