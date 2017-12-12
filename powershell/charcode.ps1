$path = $args[0]
if (!$path) {write-output "Specify a file encoded in UTF-8."; break}
if (!(test-path($path))) {write-output "$path does not exist."; break}

$file = get-content $path -encoding UTF8
$file.ToCharArray() | %{
  $dec = [int]$_
  $hex = [string]::format("{0:X4}", $dec)
  write-output "$_ `t U+$hex `t $dec"
}