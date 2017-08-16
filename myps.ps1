[CmdletBinding()]
param(
  $columns = 2,
  [alias("h")][switch] $help = $false
)

$psdir = "D:\home\bin\"

function help
{
  write-output "
  #>myps.ps1 [number of columns (up to 4)]
    -h: help
  "
}

if ($help) { help; break }

if ($columns -gt 4) {$columns = 4}

$table = New-Object system.Data.DataTable "My scripts"
$col1 = New-Object system.Data.DataColumn 1,([string])
$table.columns.add($col1)
if ($columns -ge 2) {
  $col2 = New-Object system.Data.DataColumn 2,([string])
  $table.columns.add($col2)
}
if ($columns -ge 3) {
  $col3 = New-Object system.Data.DataColumn 3,([string])
  $table.columns.add($col3)
}
if ($columns -ge 4) {
  $col4 = New-Object system.Data.DataColumn 4,([string])
  $table.columns.add($col4)
}

$filenames = get-childItem -path $psdir -file *.ps1 -name

$total = $filenames.count - 1
$cnt = 0
$flag = $true

do {
  $row = $table.NewRow()
  if ($cnt -le $total) {
    $row.1 = $filenames | select-object -index $cnt
    $cnt++
  }
  if ($cnt -lt $total) {
    if ($columns -ge 2) {
      $row.2 = $filenames | select-object -index $cnt
      $cnt++
    }
  } else {
    $flag = $false
  }
  if ($cnt -lt $total) {
    if ($columns -ge 3) {
      $row.3 = $filenames | select-object -index $cnt
      $cnt++
    }
  } else {
    $flag = $false
  }
  if ($cnt -lt $total) {
    if ($columns -ge 4) {
      $row.4 = $filenames | select-object -index $cnt
      $cnt++
    }
  } else {
    $flag = $false
  }
  $table.Rows.Add($row)
} while ($flag)

$table | format-table #-AutoSize
