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
^---	<--->
^title:	<title:>
^keywords:	<keywords:>
^tags:	<tags:>
^summary:	<summary:>
^(sidebar: .+)	<`$1>
^(language: .+)	<`$1>
^(permalink: .+)	<`$1>
^(\[comment\]: .+)	
^#####	<#####>
^####	<####>
^###	<###>
^##	<##>
^(\s*?\*)	<`$1>
^(\s*?\d.)	<`$1>
(!?\[)	<`$1>
(\]$)	<]>
(\].+?\))	<`$1>
(\{.+\})	<`$1>
^>	<&gt>
\s>\s	< &gt >
\*\*	<**>
\s_	< _>
_\s	<_ >
^_	<_>
\|	<|>"
return $this
}

function CreateUnlockTags {
$this = "old`tnew
<	
>	
&gt	>"
return $this
}

if ( $help ) { help; break }
if ( $unlock ) { $lock=$false }

if ( !$tagfile ) { 
    if ($lock) { 
      $tagfile = "md_lock.tsv"
      $tagdef = CreateLockTags
    } else {
      $tagfile = "md_unlock.tsv"
      $tagdef = CreateUnlockTags
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

foreach ($file in get-childitem *.md -recurse -file) {      
  filesearch.ps1 $file -p $tagfile
}