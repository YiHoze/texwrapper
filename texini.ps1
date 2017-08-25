#$env:TEXEDIT = "code.cmd -g %f:%l -r"
$Sumatra = "C:\Program Files\SumatraPDF\SumatraPDF.exe"
&$Sumatra -inverse-search  "`"C:\Program Files\Microsoft VS Code\code.exe`" -g %f:%l -r"

$texmfcnf="C:\texlive\2017\texmf.cnf"
$texmfhome = "TEXMFHOME = D:/home/texmf"
add-content $texmfcnf $texmfhome

write-output "
Run cmd as administrator
#> tlmgr repository list
#> tlmgr option repository http://ftp.kaist.ac.kr/tex-archive/systems/texlive/tlnet/
#> tlmgr option repository http://ftp.neowiz.com/CTAN/systems/texlive/tlnet/
#> tlmgr option repository http://ftp.ktug.org/tex-archive/systems/texlive/tlnet 
#> tlmgr update --self --all
"

#> tlmgr repository add http://ftp.ktug.org/KTUG/texlive/tlnet/ KTUG
#> tlmgr pinning add KTUG "*"
# http://ftp.neowiz.com/CTAN/systems/texlive/Images/
# http://ftp.kaist.ac.kr/tex-archive/systems/texlive/Images/
