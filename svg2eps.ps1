$files = $args[0]
$extraoption = $args[1]
if ( !($files) ) { write-output "svg2eps.ps1 foo.svg [-p]"; break}

get-childitem -name $files | foreach-object {
  &"C:\Program Files\LibreOffice 5\program\soffice.exe" --convert-to eps $_
  if ( $? -eq $true -and $extraoption ) {
    $file = $_
    switch ($extraoption) {
      default {}
      "-p" {
        $eps = $file.split('.')[0] + ".eps"
        epstopdf $eps
      }
    }
  }
}
