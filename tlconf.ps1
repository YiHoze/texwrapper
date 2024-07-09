[CmdletBinding()]
param (
    [alias('h')][switch] $help = $false,
    [alias('b')][switch] $build = $false,
    [alias('c')][switch] $cache = $false,
    [alias('u')][switch] $update = $false
)

try {
    $texmfroot = &kpsewhich -var-value=TEXMFROOT
} catch {
    Write-Output "TeX Live is not found. Aborted."
    Exit
}

$LocalConfPath = Join-Path $texmfroot -ChildPath "texmf-var\fonts\conf\local.conf"
$LocalConfContent = "<dir>C:/Users/{0}/AppData/Local/Microsoft/Windows/Fonts</dir>" -f $env:USERNAME
$SumatraPDFpath = "C:\Users\{0}\AppData\Local\SumatraPDF\SumatraPDF.exe" -f $env:USERNAME
$InverseSearch = 'code.exe -r -g "%%f:%%l"'


$global:TeXLive = @{
    TEXMFHOME = "C:\home\texmf";
    TEXEDIT = 'code.exe -r -g "%%s:%%d"';
    LocalConfPath = $LocalConfPath;
    LocalConfContent = $LocalConfContent;
    SumatraPDFpath = $SumatraPDFpath;
    InverseSearch = $InverseSearch;
    MainRepository = "http://mirror.navercorp.com/CTAN/systems/texlive/tlnet/";
    PrivateRepository = "https://mirror.ischo.org/KTUG/texlive/tlnet/"
}
# MainRepository = "http://mirror.kakao.com/CTAN/systems/texlive/tlnet/"
# PrivateRepository = "http://ftp.ktug.org/KTUG/texlive/tlnet/"
# MainRepository = "https://cran.asia/tex/systems/texlive/tlnet/"
# PrivateRepository = "https://cran.asia/KTUG/texlive/tlnet/"

function help { 
    write-output "Set by default: TEXMFHOME, TEXEDIT, inverse-search, local.conf, repositories
    -b: Build formats anew.
    -c: Cache fonts for XeTeX and LuaTeX.
    -u: Update the TeX Live."
}

function SetTEXMFHOME {
    set-itemproperty -path HKCU:\\Environment -name TEXMFHOME -value $global:TeXLive.TEXMFHOME
    Write-Output "TEXMFHOME:"
    (get-itemproperty -path HKCU:\\Environment)."TEXMFHOME"
}

function SetTEXEDIT {
    set-itemproperty -path HKCU:\\Environment -name TEXEDIT -value $global:TeXLive.TEXEDIT
    write-output "TEXEIDT:"
    (get-itemproperty -path HKCU:\\Environment)."TEXEDIT"
}

function SetSumatraPDF {
    if (Test-Path $global:TeXLive.SumatraPDFpath) {
        $cmd = "{0} -inverse-search '{1}'" -f $global:TeXLive.SumatraPDFpath, $global:TeXLive.InverseSearch
        Invoke-Expression $cmd
    } else {
        Write-Output "{0} is not found." -f $global:TeXLive.SumatraPDFpath
    }
}

function CreateLocalconf {
    Set-Content -Path  $global:TeXLive.LocalConfPath -Value $global:TeXLive.LocalConfContent
    (Get-ChildItem $global:TeXLive.LocalConfPath).FullName
    Get-Content $global:TeXLive.LocalConfPath
}

function SetRepository {
    tlmgr.bat option repository $global:TeXLive.MainRepository
    tlmgr.bat repository add $global:TeXLive.PrivateRepository private
    tlmgr.bat pinning add private "*"
}

if ($help) { help }
elseif ($build) { 
    fmtutil-sys --all
}
elseif ($cache) { 
    fc-cache.exe -v -r
    luaotfload-tool --update --force --verbose=3
}
elseif ($update) { 
    tlmgr.bat update --self --all
}
else {
    SetTEXMFHOME
    SetTEXEDIT
    SetSumatraPDF
    CreateLocalconf
    SetRepository
}