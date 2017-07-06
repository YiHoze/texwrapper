# Remove tex auxiliary files
$files = @("aux", "idx", "ilg", "ind", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "vrb")
foreach ($element in $files) 
{
	if (Test-Path("*.$element")) { remove-item "*.$element" }
}
if (Test-Path("_minted*")) { remove-item "_minted*" -recurse }
if (test-path("tempverb.tex")) { remove-item "tempverb.tex" }