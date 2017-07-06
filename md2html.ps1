#pandoc -s -f markdown_github -t html -o foo.html foo.md
#pandoc -f html -t markdown_github --atx-headers -o foo.md foo.html

$option = $args[0]

function md2html {
  foreach ($source in get-childitem *.md -recurse -file) {  
    $target = $source.directoryname + "\" + $source.basename + ".html"
    pandoc -s -f markdown_github -t html -o $target $source
 }
}

function html2md {
  foreach ($source in get-childitem *.html -recurse -file) {  
    $target = $source.directoryname + "\" + $source.basename + ".md"
    pandoc -f html -t markdown_github --atx-headers -o $target $source
 }
}

function howto {
write-output "
md2html.ps1 -h/-m/-rh/-rm
  -h: convert md to html
  -m: convert html to md
  -rh: remove html
  -rm: remove md
"
}

switch ($option) {
  "-h" { md2html }
  "-m" { html2md }
  "-rh" { get-childitem *.html -recurse -file | remove-item }
  "-rm" { get-childitem *.md -recurse -file | remove-item }
  default { howto }
}