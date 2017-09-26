# git config --global user.name YiHoze
# git config --global user.email yihoze@icloud.com
# git init
# git status
# git add foo OR git add .
# git commit -m "comment"
# git remote add origin https://github.com/YiHoze/bin.git
# git remote add origin https://github.com/YiHoze/HzGuide.git
# git push -u origin master

[CmdletBinding()]
param(
	[alias("b")][switch] $bin=$false,
	[alias("t")][switch] $KTS=$false,
	[alias("z")][switch] $hzguide=$false,
	[alias("c")][string] $comment,
	[alias("h")][switch] $help=$false
)

function help 
{
write-output "
#>gitpush.ps1 repository [comment]
#>gitpush.ps1 -z -c `"blah blah`"  
  -b: push 'D:\home\bin' to https://github.com/YiHoze/bin.git
  -t: push 'D:\home\doc\KTS\KTSmemo' to  https://github.com/KoreanTUG/KTSmemo.git
  -z: push 'D:\home\texmf\tex\latex\hzguide' to  https://github.com/YiHoze/HzGuide.git
  -c: comment for commit (current date and time by default)
  -h: help
"
}

if ($help) { help; break }


if( !($comment) ) { 	
	$comment = get-date -UFormat "%Y-%m-%d_%R"
} 

$repo = $false

if ($bin) {
	set-location "D:\home\bin"
	$repo = $true
} elseif ($KARI) {
	set-location "D:\pyFlutter\docs"
	$repo = $true
} elseif ($KTS) {
	set-location "D:\home\doc\KTS\KTSmemo"
	$repo = $true
} elseif ($hzguide) {
	set-location "D:\home\texmf\tex\latex\hzguide"
	$repo = $true
}

if ($repo) {
	git add *
	git commit -m $comment
	if (!$KARI) {
		git push origin master
	}
} else {
	help
}
