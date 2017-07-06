if(!($args[0])){
	write-output "usage:pdfimg foo.pdf [counter]"
	break
}

$file = $args[0]
$cnt = $args[1]
if(!($cnt)) {
	$cnt = "cnt"
} 

pdfimages -j $file $cnt
imgconvert *.ppm png
remove-item *.ppm