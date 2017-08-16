[CmdletBinding()]
param(
	[string] $job = "manual",
	[alias("c")][switch] $compile = $false,
	[alias("h")][switch] $help = $false
)

function help
{
write-output "
#>myscenario.ps1 [job name] [option]
  -c: make PDF
  -h: help
"
}

if ($help) { help; break }

$tex = $job + ".tex"
$pdf = $job + ".pdf"

if (Test-Path($tex)) {
	Write-Output "$tex already exsits."
	$answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
	if ($answer -ne 'y') {
		Write-Output "This job is canceled"; break
	}
}

Function prototype () {
$this="\documentclass[10pt,openany]{hzguide}`n
\LayoutSetup{paper=A4, column=vartwo}
\DecolorHyperlinks`n
\title{Operation Manual}
\date{}`n
\begin{document} `n
\begin{IfVartwoEnlarge}
\maketitle
\end{IfVartwoEnlarge}
\thispagestyle{empty}`n
\newpage
\SectionNewpageOn`n
\tableofcontents*`n
\chapter{Introduction}`n\scenepara`n
\section{Features}`n\scenelist`n
\section{Package Items}`n\sceneimagetable`n
\section{Specifications}`n\scenespectables`n
\chapter{Safety}`n
\section{General Precautions}`n\scenelist[itemize][itemize]`n
\section{Tools}`n\sceneimagetable`n
\section{Safety Gear}`n\sceneimagetable`n
\chapter{Installation}`n
\section{Installation Requirements}`n\scenelist`n
\section{Installing X}`n\sceneprocedure[5]`n
\section{Checking X}`n\sceneprocedure`n
\section{Starting X}`n\scenelist*`n
\chapter{Operation}`n\scenetasks`n
\chapter{Troubleshooting}`n\listofproblems*`n\sceneproblems`n
\chapter{Maintenance}`n
\section{Precautions for Maintenance}`n\scenelist`n
\section{Scheduled Inspection}`n\scenelist`n
\chapter{Warranty}`n
\section{Warranty Coverage}`n\scenepara*`n
\section{Limitation of Liability}`n\scenepara*\scenelist`n
\section{Contact Information}`n\scenepara*`n
\appendix`n
\chapter{Technical Information}`n\scenespectables`n
\chapter{Glossary}`n\scenelist[terms]`n
\end{document}"
return $this
}

Switch ($jobtype) {
	default {$content = prototype}
}

Set-Content $tex -Encoding UTF8 $content

if ($compile) {
	xlt.ps1 $tex -b
	xlt.ps1 $tex -b
	open.ps1 $pdf 
}
open.ps1 $tex 
