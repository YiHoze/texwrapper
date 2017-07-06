# Extract words from a text file

$file = $args[0]
$dic = $args[1]
if (!($file)) {write-output "usage: WordExtract.ps1 foo.txt [foo_dic.txt]"; break}
if (!(test-path($file))) {write-output "$file does not exist."; break}
if (!($dic)) {	
	$dic = (get-item $file).fullname
	$dic = $dic.substring(0,$dic.LastIndexOf('\')+1)
	$dic = $dic + (get-item $file).basename + "_dic.txt"	
}
$src = Get-Content $file -encoding UTF8
$Dictionary = @{}
$src | foreach {
    $Line = $_
    $Line.Split(" .,:;?!*/()[]{}-```"`t`#%$\") | foreach {	#"
		$Word = $_
        If (!$Dictionary.ContainsKey($Word)) {
            $Dictionary.Add($Word, 1)
        }
    } 
}
$Dictionary.keys.GetEnumerator() | sort-object | set-content $dic -encoding UTF8
Write-output "See $dic."