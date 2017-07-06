function procede(){
 if ($? -eq $true) {
  $answer = Read-Host "Continue to install others? (Enter Y or N)"
  if (($answer -eq 'y') -or ($answer -eq 'Y')) {
    return
  } else {	
    Write-Output "Installation is canceled"; break
  }
 } else {
  break
 }
}

procede

#&"D:\home\Installers\Acrobat_Pro_DC"

# Adobe CS6
#&"D:\home\Installers\Creative_Suite_6\Adobe CS6\Set-up.exe"
#procede

&"D:\home\Installers\emeditor11\emed64_11.0.2.exe"
procede

#&"D:\home\Installers\reserve"

# Atom
&"D:\home\Installers\AtomSetup-x64.exe"
procede

# Bandizip
&"D:\home\Installers\BANDIZIP-SETUP.EXE"
procede

# ConEmu
&"D:\home\Installers\ConEmuSetup.170326.exe"
procede

#&"D:\home\Installers\fontmatrix-0.6.0-win32.exe"

# FreeCommander
&"D:\home\Installers\FreeCommanderXE-32-en-public_setup.exe"
procede

# Git
&"D:\home\Installers\Git-2.12.2-64-bit.exe"
procede

# GitHub Desktop
&"D:\home\Installers\GitHubSetup.exe"
procede

# GhostScript
&"D:\home\Installers\gs921w64.exe"
procede

# ImageMagick
&"D:\home\Installers\ImageMagick-7.0.5-4-Q16-x64-dll.exe"
procede

# Tex Live 2016
&"D:\home\Installers\install-tl-windows.exe"
procede

# LibreOffice
&"D:\home\Installers\LibreOffice_5.3.1_Win_x64.msi"
procede

# Listary
&"D:\home\Installers\Listary.exe"
procede

# PDFtk
&"D:\home\Installers\pdftk_free-2.02-win-setup.exe"
procede

# Sumatra PDF
&"D:\home\Installers\SumatraPDF-3.1.2-64-install.exe"
procede

# TortoiseSVN
#&"D:\home\Installers\TortoiseSVN-1.7.10.23359-x64-svn-1.7.7.msi"
#procede

# WinPython
&"D:\home\Installers\WinPython-64bit-3.5.2.2Qt5.exe"
procede