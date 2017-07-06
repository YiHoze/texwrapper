$global:files=''
$global:option=''
$global:today=''

if($args[0] -ne $null) { $files=$args[0] }
else { write-output "today.ps1 *.foo [-r] [yyyy-mm-dd]"; break }

function AppendDate () {
  get-childitem $files | 
  foreach-object { 
    $newname = $_.basename + $today + $_.extension
    rename-item $_.name $newname
  }
}

function RemoveDate () {
  get-childitem $files |
  foreach-object {
    if ( $_.name.contains($today) ) {
      $oldname = $_.name
      $newname = $oldname.replace($today, "")
      rename-item $_.name $newname
    }    
  }
}

function SetOption($this) {
  if($this -eq "-r") { $global:option=$this }
  else { $global:today=$this}
}

if($args[1] -ne $null) { SetOption($args[1]) }
if($args[2] -ne $null) { SetOption($args[2]) }

if( !($today) ) { 
  $today = get-date -format "yyyy-MM-dd" 
  $today = "_" + $today
}

#write-output "$files $option $today"

switch ($option) {
  "-r"  { RemoveDate }
  default  { AppendDate }
}