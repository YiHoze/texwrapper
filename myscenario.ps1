if (!($args[0]) -or ($args[0].StartsWith('-'))) {
	$job=$args[1]
	$jobtype = $args[0]
} else {
	$job = $args[0]
	$jobtype = $args[1]
}

if (!($job)) {$job = "manual"}
$tex = $job + ".tex"
$pdf = $job + ".pdf"

if (Test-Path($tex)) {
Write-Output "$tex already exsits."
$answer = Read-Host "Do you want to overwrite it? (Enter Y or N)"
if (($answer -ne 'y') -or ($answer -ne 'Y')) {Write-Output "This job is canceled"; break}
}

Function prototype () {
$this="\documentclass[10pt,openany]{hzguide}
\LayoutSetup{paper=A4, column=vartwo}
\DecolorHyperlinks
\title{X Installation \& Operation Manual}
\date{}
\begin{document} 
\begin{IfVartwoEnlarge}
\maketitle
\end{IfVartwoEnlarge}
\thispagestyle{empty}
\newpage
\SectionNewpageOn
\tableofcontents*
\chapter{Introduction}\scenepara
\section{Features}\scenelist
\section{Package~Items}\sceneimagetable
\section{Specifications}\scenespectables
\chapter{Safety}
\section{General~Precautions}\scenelist[itemize][itemize]
\section{Tools}\sceneimagetable
\section{Safety~Gear}\sceneimagetable
\chapter{Installation}
\section{Installation~Requirements}\scenelist
\section{Installing~X}\sceneprocedure[5]
\section{Checking~X}\sceneprocedure
\section{Starting~X}\scenelist*
\chapter{Operation}\scenetasks
\chapter{Troubleshooting}\sceneproblems
\chapter{Maintenance}
\section{Precautions~for~Maintenance}\scenelist
\section{Scheduled~Inspection}\scenelist
\chapter{Warranty}
\section{Warranty~Coverage}\scenepara*
\section{Limitation~of~Liability}\scenepara*\scenelist
\section{Contact~Information}\scenepara*
\appendix
\chapter{Technical~Information}\scenespectables
\chapter{Glossary}\scenelist[terms]
\end{document}"
return $this
}

Switch ($jobtype) {
	default {$content = prototype}
}

Set-Content $tex -Encoding UTF8 $content
xpub.ps1 $tex -b
xpub.ps1 $tex -b
open.ps1 $tex 
open.ps1 $pdf 