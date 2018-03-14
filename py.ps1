# If the specified python script is not found in the current directory, this directory will be searched for it.
$pydir = "D:\home\bin\"

$pyfile = $args[0]
if (! $pyfile) {
    write-output "Specify a python script to run."
    break
} else {
    if (! ($pyfile.EndsWith(".py"))) { $pyfile = $pyfile + ".py" }
}

# Check if the specified python script exists.
$pypath = $pyfile
if (! (test-path($pypath))) {
    $pypath = $pydir + $pyfile
} 
if (! (test-path($pypath))) {
    write-output "$pyfile is not found."
    break
}

# Gather arguments to pass them to the specified python script.
$pyarg = ""
if ($args.Count -gt 1) {
    for ($i=1; $i -le $args.Count; $i++) {
        $pyarg = $pyarg + " " + $args[$i]
    }
    $cmd = "python $pypath $pyarg"
} else {
    $cmd = "python $pypath"
}

Invoke-Expression $cmd