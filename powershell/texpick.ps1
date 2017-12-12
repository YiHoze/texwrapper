$tex=$args[0]
$output=$args[1]

if ( ! $tex ) {
	write-output "TexPick.ps1 foo.tex [result.txt]"; break
} else {
	if (!($tex.contains('*'))) {
		if (!(test-path($tex))) {write-output "$tex does not exist."; break}
	}
}

if ( ! $output ) { $output="result.txt" }

$command=@("\\.\ ", "\\[a-zA-Z]*")

function FindCommand ($this) {
	$command | foreach-object {
		if($this -match $_) {
			$match = $matches[0]
			add-content $output $match -encoding UTF8
		}
	}
}

function FindEnvironment ($this) {
	if (  $this -match "\\begin\{.+?\}" ) {
		$match = $matches[0]
		$strbegin = $match.indexof("{") + 1
		$strend = $match.indexof("}")
		$strlength = $strend - $strbegin
		$str = $match.substring($strbegin, $strlength)
		add-content $output $str -encoding UTF8
	}
}

if ( test-path($output) ) {
	remove-item $output
}

foreach ($this in get-childitem $tex -name) {
	(get-content $this -encoding UTF8) | foreach-object {
		FindCommand($_)
		FindEnvironment($_)
	}
}

get-content $output | sort-object -unique | set-content $output -encoding UTF8
