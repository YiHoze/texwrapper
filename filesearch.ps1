[CmdletBinding()]
param(
  [string] $files,
  [alias("s")][string] $str,
  [alias("d")][string] $delimiter,
  [alias("n")][string] $new,
  [alias("p")][string] $pattern,
  [alias("r")][switch] $recursive=$false,
  [alias("h")][switch] $help=$false
)

function help {
  write-output "
  Search for or replace strings
  Usage:
    #>filesearch.ps1 target_file -s string
    #>filesearch.ps1 target_file -s old_string -n new_string
    #>filesearch target_file -p pattern_file.tsv
  Options:
    -s: string to search for
    -d: delimiter to split by
    -n: new string to replace with
    -p: pattern file (.tsv)
    -r: recursive (including subdirectories)
    -h: help
"
}

function checkcmd () {
  if ($help -or !$files ) { help; break }
  if (!$str -and !$pattern) { help; break }
  if (!($files.contains('*'))) {
    if (!(test-path($files))) { write-output "$files does not exist."; break}
  }
  if ($pattern) {
    if (!(test-path($pattern))) {write-output "$pattern does not exist."; break }
  }
}

function SearchPhrase {
  foreach ($file in get-childitem $files) {
    (get-content $file -encoding UTF8) | foreach-object {
        if($_ -match $str) {
          write-output $_.split($delimiter)
        }
    }
  }
}

function SearchLine {
  foreach ($file in get-childitem $files) {
    $filename = split-path $file -leaf
    write-output $filename
    get-content $file -encoding UTF8 |
      select-string -pattern $str |
        select-object linenumber, line | format-list
  }
}

function SingleReplace {
  foreach ($file in get-childitem $files) {
      $content = get-content $file -encoding UTF8 -ReadCount 0
      $content -replace $str, $new | set-content $file -encoding UTF8
  }
}

function SingleReplaceRecursive {
  foreach ($file in get-childitem $files -recurse) {
      $content = get-content $file -encoding UTF8 -ReadCount 0
      $content -replace $str, $new | set-content $file -encoding UTF8
  }
}

function MultipleReplace () {
  foreach ($file in get-childitem $files) {
    $patterns = import-csv $pattern -delimiter "`t" -encoding UTF8
    foreach ($item in $patterns) {
      $str = $item.old
      $new = $item.new
      $content = get-content $file -encoding UTF8 -ReadCount 0
      $content -replace $str, $new | set-content $file -encoding UTF8
    }
  }
}

function MultipleReplaceRecursive () {
  foreach ($file in get-childitem $files -recurse) {
    $patterns = import-csv $pattern -delimiter "`t" -encoding UTF8
    foreach ($item in $patterns) {
      $str = $item.old
      $new = $item.new
      $content = get-content $file -encoding UTF8 -ReadCount 0
      $content -replace $str, $new | set-content $file -encoding UTF8
    }
  }
}

checkcmd

if (! $pattern) {
  if (! $new) {
    if (! $delimiter ) {
      SearchLine
    } else {
      SearchPhrase
    }
  } else {
    if (! $recursive) {
      SingleReplace
    } else {
      SingleReplaceRecursive
    }
  }
} else {
  if (! $recursive) {
    MultipleReplace
  } else {
    MultipleReplaceRecursive
  }
}
