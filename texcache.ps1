# [CmdletBinding()]
# param(
#     [alias("c")][switch] $clear = $false,
#     [alias("h")][switch] $help = $false
# )

# if ($help) {
# write-output "
# #>texcache.ps1 [option]
#   -c: clear all font caches before re-caching
#   -h: help
# "
# break
# }

# if ($clear) {
#     remove-item C:\texlive\2016\texmf-var\fonts\cache\*.*
# }
# fc-cache -f -v

remove-item C:\texlive\2016\texmf-var\fonts\cache\*.*
fc-cache -f -v
