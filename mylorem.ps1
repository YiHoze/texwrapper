[CmdletBinding()]
param(
	[string] $file,
	[alias("t")][string] $text,
	[alias("c")][string] $count,
	[alias("h")][switch] $help=$false
)


function help
{
	write-output "
	#>mylorem.ps1 filename -c count -t text
	"
}

if ($help) { 	help; break }

if ( !($file) ) { $file = "lorem.txt" }
if ( !($count) ) { $count = 100 }
if ( !($text) ) { $text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Etiam lobortis facilisis sem. Nullam nec mi et neque pharetra sollicitudin. Praesent imperdiet mi nec ante."}

if ( test-path($file) ) { remove-item $file }

for ($i=1; $i -le $count; $i++) {
	add-content $file -encoding UTF8 $text
}
