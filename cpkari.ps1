[CmdletBinding()]
param(
    [alias("r")][switch]$remove=$false
)

if ($remove) {
    remove-item D:\pyFlutter\docs\manual\_build\latex\hzguide.cls 
    remove-item D:\pyFlutter\docs\manual\_build\latex\karisphinx.sty 
    remove-item D:\pyFlutter\docs\tutorial\_build\latex\hzguide.cls 
    remove-item D:\pyFlutter\docs\tutorial\_build\latex\karisphinx.sty 
    remove-item D:\pyFlutter\docs\howto\_build\latex\hzguide.cls 
    remove-item D:\pyFlutter\docs\howto\_build\latex\karisphinx.sty 
} else {
    copy-item D:\home\texmf\tex\latex\hzguide\hzguide.cls D:\pyFlutter\docs\_templates -force
    copy-item D:\home\texmf\tex\latex\kari\karisphinx.sty D:\pyFlutter\docs\_templates -force
    copy-item D:\home\texmf\tex\latex\hzguide\hzguide.cls D:\pyFlutter\docs\manual\_build\latex -force
    copy-item D:\home\texmf\tex\latex\kari\karisphinx.sty D:\pyFlutter\docs\manual\_build\latex -force
    copy-item D:\home\texmf\tex\latex\hzguide\hzguide.cls D:\pyFlutter\docs\tutorial\_build\latex -force
    copy-item D:\home\texmf\tex\latex\kari\karisphinx.sty D:\pyFlutter\docs\tutorial\_build\latex -force
    copy-item D:\home\texmf\tex\latex\hzguide\hzguide.cls D:\pyFlutter\docs\howto\_build\latex -force
    copy-item D:\home\texmf\tex\latex\kari\karisphinx.sty D:\pyFlutter\docs\howto\_build\latex -force
}