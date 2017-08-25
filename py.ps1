$pydir = "D:\home\bin\python\"

$pyfile = $args[0]
if (! $pyfile) {
  write-output "Specify a python script to run."
  break
} else {
  if (! ($pyfile.EndsWith(".py"))) {$pyfile = $pyfile + ".py"}
  $pypath = $pydir + $pyfile
}

if (test-path($pypath)) {
  python $pypath $args[1]
} else {
  write-output "$pyfile is not found."
}
