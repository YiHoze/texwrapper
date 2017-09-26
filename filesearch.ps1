[CmdletBinding()]
param(
    [string] $files,
    [alias("s")][string] $str,
    [alias("d")][string] $delimiter,
    [alias("n")][string] $new,
    [alias("e")][switch] $entireline = $false,
    [alias("c")][switch] $removeline = $false,
    [alias("p")][string] $pattern,
    [alias("r")][switch] $recursive = $false,
    [alias("h")][switch] $help = $false
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
        -e: replace the entire of matched line
        -c: remove matched lines
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

function SearchPhraseRecursive {
    foreach ($file in get-childitem $files -recurse) {
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

function SearchLineRecursive {
    foreach ($file in get-childitem $files -recurse) {
        $filename = split-path $file -leaf
        write-output $filename
        get-content $file -encoding UTF8 |
            select-string -pattern $str |
                select-object linenumber, line | format-list
    }
}

function SingleReplaceEach ($file)
{
    $tmpfile = "t@mp.tmp"
    if (test-path($tmpfile)) {
        Remove-Item $tmpfile
    }
    if ($removeline) {
        Get-Content $file -Encoding UTF8 |
            Where-Object { $_ -notmatch $str } |
                Set-Content $tmpfile -Encoding UTF8
        Remove-Item $file
        Rename-Item $tmpfile $file
    } elseif ($entireline) {
        get-content $file -encoding UTF8 | foreach-object {
            if($_ -match $str) {
                $_ -replace $_, $new | Out-File $tmpfile -Append
            } else {
                $_ | Out-File $tmpfile -Append
            }
        }
        Remove-Item $file
        Rename-Item $tmpfile $file    
    } else {   
        $content = get-content $file -encoding UTF8 -ReadCount 0
        $content -replace $str, $new | set-content $file -encoding UTF8    
    }
}

function SingleReplace {
    foreach ($file in get-childitem $files) {
        SingleReplaceEach($file)
    }
}

function SingleReplaceRecursive {
    foreach ($file in get-childitem $files -recurse) {
        SingleReplaceEach($file)
    }
}


function MultiReplaceEach ($file)
{
    $patterns = import-csv $pattern -delimiter "`t" -encoding UTF8
    foreach ($item in $patterns) {
        $str = $item.old
        $new = $item.new
        $content = get-content $file -encoding UTF8 -ReadCount 0
        $content -replace $str, $new | set-content $file -encoding UTF8        
    }
}

function MultipleReplace () {
    foreach ($file in get-childitem $files) {
        MultiReplaceEach($file)
    }
}

function MultipleReplaceRecursive () {
    foreach ($file in get-childitem $files -recurse) {
        MultiReplaceEach($file)
    }
}

checkcmd

if ($pattern) {
        if ($recursive) { MultipleReplaceRecursive } else { MultipleReplace }
} else {    
        if ($new -or $removeline) {
            if ($recursive) { SingleReplaceRecursive } else { SingleReplace }
        } else {
            if ($delimiter) { 
                 if ($recursive) { SearchPhraseRecursive } else { SearchPhrase }
            } else { 
                 if ($recursive) { SearchLineRecursive } else { SearchLine }
            }
        }
}
