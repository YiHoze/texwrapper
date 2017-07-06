$file =$args[0]
if ( !($file) ) { 
  write-output "usage: imginfo ImageFile"
  break
}
if ( !(test-path($file)) ) { write-output "$file does not exist."; break }
$imginfo = magick identify -verbose $file 2>&1 
(write-output $imginfo)[4 .. 7]