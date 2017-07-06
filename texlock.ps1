[CmdletBinding()] 
param(  
  [alias("l")][switch] $lock=$true,
  [alias("u")][switch] $unlock=$false,
  [alias("t")][string] $tagfile,
  [alias("h")][switch] $help=$false
)

function help {
write-output "
mdlock.ps1 options
  -l: lock markdown tags (default)
  -u: unlock markdown tags
  -t: tag file (.tsv)
  -h: help
"
}

function CreateLockTags {
$this = "old`tnew
^(%.+)	
<	&lt
>	&gt
(\\documentclass.+)	<`$1>
(\\usepackage.+)	<`$1>
(\\SetDocType.+)	<`$1>
(\\begin.+)	<`$1>
(\\end.+)	<`$1>
\\chapter\{(.+?)\}	<\chapter{>`$1<}>
\\section\{(.+?)\}	<\section{>`$1<}>
\\section\*\{(.+?)\}	<\section*{>`$1<}>
\\subsection\{(.+?)\}	<\subsection{>`$1<}>
\\subsection\*\{(.+?)\}	<\subsection*{>`$1<}>
\\topic\{(.+?)\}	<\topic{>`$1<}>
\\topic\*\{(.+?)\}	<\topic*{>`$1<}>
\\task\{(.+?)\}	<\topic{>`$1<}>
\\item\[(.+?)\]	<\item[>`$1<]>
\\Sub\{(.+?)\}	<\Sub{>`$1<}>
\\Sup\{(.+?)\}	<\Sup{>`$1<}>
(\\label.+?\})	<`$1>
(\\ref.+?\})	<`$1>
(\\pageref.+?\})	<`$1>
(\\titleref.+?\})	<`$1>
(\\foreign.+?\})	<`$1>
(\\placeimage.+?\})	<`$1>
(\\illuenum.+?\}\{)	<`$1>
(\\input.+?\})	<`$1>
(\\commoninput.+?\})	<`$1>
(\\vspace.+?\})	<`$1>
(\\ui.+?\})	<`$1>
(\\lineimg.+?\})	<`$1>
(\\uitem.+?\])	<`$1>
\\item\s	"<\item> "
\s&	" <&>"
\\%	<\%>
\\\\	<\\>
\\appendix	<\appnedix>
\\FrontCover	<\FrontCover>
(\\tableofcontents\*?)	<`$1>
\\BackCover	<\BackCover>
\\newpage	<\newpage>
\\EnlargePage	<\EnlargePage>
\\TableHeadFont	<\TableHeadFont>
\\hline	<\hline>
\\CoverInfoSetup\{	<\CoverInfoSetup{>
(CoverImage.+?\})	<`$1>
ModelName=\{(.+?)\}	<ModelName={>`$1<}>
ProductType=\{(.+?)\}	<ProductType={>`$1<}>
DocumentName=\{(.+?)\}	<DocumentName={>`$1<}>
RevisionInfo=\{(.+?)\}	<RevisionInfo={>`$1<}>
CoverNote=\{(.+?)\}	<CoverNote={>`$1<}>
(\\def.+?\{)	<`$1>
(\\newcommand.+?\{)	<`$1>
(\\footnotetext.+?\{)	<`$1>
^\}	<}>
\}$	<}>
&gt	<&gt>
&lt	<&lt>"
return $this
}

function CreateUnLockTags {
$this = "old`tnew
<	
>	
&gt	>
&lt	<"
return $this
}

if ( $help ) { help; break }
if ( $unlock ) { $lock=$false }

if ( !$tagfile ) { 
    if ($lock) { 
      $tagfile = "tex_lock.tsv"
      $tagdef = CreateLockTags
    } else {
      $tagfile = "tex_unlock.tsv"
      $tagdef = CreateUnLockTags
    }
    if ( !(test-path($tagfile)) ) {
      $answer = read-host "Do you want to create the tag definition file by default? (Enter Y or N)"
      if (($answer -eq 'y') -or ($answer -eq 'Y')) {  
        set-content $tagfile -encoding UTF8 $tagdef
      } else {
        break 
      }
    }
}

foreach ($file in get-childitem *.tex -recurse -file) {      
  filesearch.ps1 $file -p $tagfile 
}
