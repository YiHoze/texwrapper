$texmfcnf="C:\texlive\2016\texmf.cnf"
$fontsconf="C:\texlive\2016\texmf-var\fonts\conf\fonts.conf"

# $env:TEXEDIT = "emeditor.exe /l `%d `%s"
#&"C:\Program Files (x86)\SumatraPDF\sumatrapdf.exe" -inverse-search `"C:\Program Files\EmEditor\emeditor.exe /l `%l `%f`"

$texmfhome = "OSFONTDIR = $SystemRoot/fonts/;D:/home/fonts/
TEXMFHOME = D:/home/texmf"
add-content $texmfcnf $texmfhome

$homefonts = "<?xml version=`"1.0`"?> 
<!DOCTYPE fontconfig SYSTEM `"fonts.dtd`">  
<fontconfig>  
<dir>C:/Windows/Fonts</dir>  
<dir>C:/texlive/2015/texmf-dist/fonts/opentype</dir>  
<dir>C:/texlive/2015/texmf-dist/fonts/truetype</dir>  
<dir>C:/texlive/texmf-local/fonts/opentype</dir>  
<dir>C:/texlive/texmf-local/fonts/truetype</dir>  
<dir>D:/home/fonts/opentype</dir>  
<dir>D:/home/fonts/truetype</dir>  
</fontconfig>"
set-content $fontsconf $homefonts

# cmd에서 관리자 모드로 실행해야
# tlmgr repository remove main
# tlmgr repository add http://ftp.ktug.org/tex-archive/systems/texlive/tlnet main
# tlmgr option repository http://ftp.neowiz.com/CTAN/systems/texlive/tlnet/
tlmgr option repository http://ftp.ktug.org/tex-archive/systems/texlive/tlnet 
tlmgr repository add http://ftp.ktug.org/KTUG/texlive/tlnet/ KTUG
tlmgr pinning add KTUG "*"
# tlmgr repository list
tlmgr update --self --all
tlmgr install graphicsonthefly hangulfontset hanjacnt hcr-lvt hnja2hngl ifpxltex jiwonlipsum kocircnum kotex-euc kotex-midkor kotex-sections ksbaduk ksforloop ksmisc kswrapfig nanumbaruntype1 nanumttf ob-chapstyles readhanja unfonts-base unfonts-extra ktugbin texworks-config
# luaotfload-tool --update
# luaotfload-tool --uvvv