[CmdletBinding()]
param(
    [string] $font,
    [alias("s")][string] $sample="d:\home\bin\fonttype.txt",
	[alias("o")][string] $output,
	[alias("h")][switch] $help = $false
)

function help
{
Write-Output "
#>fonttypeface.ps1 font_name [option]
Useage:
fonttypeface.ps1 `"Linux Libertine O`" LinuxLibertine [FFFF]
Option:
    -s: sample text file
	-o: output filename 
	-h: help
"
}

if (!$font -or $help) { help; break }

if (!$output) {
	$output = $font.Substring(0, 5)
}
if (!($output.EndsWith(".tex"))) {
    $output = $output + ".tex"    
}
if (test-path $output) { remove-item $output }

$beforestr = "
\documentclass{minimal}
\usepackage{fontspec}
\setmainfont{$font}
\setlength\parskip{1.5\baselineskip}
\setlength\parindent{0pt}
\begin{document}"
$afterstr = "\end{document}"

add-content $output -Value $beforestr -Encoding UTF8
$content = get-content $sample -Encoding UTF8
add-content $output -Value $content -Encoding UTF8
add-content $output -Value $afterstr -Encoding UTF8

 xelatex $output
 texclean.ps1
 Remove-Item $output