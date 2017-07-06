# git config --global user.name YiHoze
# git config --global user.email yihoze@icloud.com
# git init
# git status
# git add foo OR git add .
# git commit -m "comment"
# git remote add origin https://github.com/YiHoze/latex.git
# git remote add origin https://github.com/YiHoze/powershell_scripts.git
# git push origin master

[CmdletBinding()]
param(
	[alias("b")][switch] $bin=$false,
	[alias("l")][switch] $latex=$false,
	[alias("c")][string] $comment,
	[alias("h")][switch] $help=$false
)

function help 
{
	write-output "
	-b: push 'D:\home\bin' to https://github.com/YiHoze/bin.git
	-l: push 'D:\home\texmf\tex\latex' to  https://github.com/YiHoze/latex.git
	-c: comment for commit
	-h: help
	"
}

if ($help) { help; break }


if( !($comment) ) { 	
	$comment = get-date -UFormat "%Y-%m-%d_%R"
}

if ($powershell) {
	set-location "D:\home\bin"
	git add *
	git commit -m $comment
	git push origin master
}

if ($latex) {
	set-location "D:\home\texmf\tex\latex"
	git add *
	git commit -m $comment
	git push origin master
}