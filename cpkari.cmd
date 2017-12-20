@echo off
del  C:\texlive\texmf-local\tex\latex\local\*.* /y
copy C:\home\texmf\tex\latex\hzguide\hzguide.cls  C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\texmf\tex\latex\kari\karijupyter.sty C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\texmf\tex\latex\kari\karisphinx.sty  C:\PROJECTS\KARI\docs\bin\ /y

copy C:\home\bin\docenv.ini      C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\kari.tplx       C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\strpattern.tsv  C:\PROJECTS\KARI\docs\bin\ /y

copy C:\home\bin\autojosa.exe    C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\bmind.exe       C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\docbuild.exe    C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\imginfo.exe     C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\imgsize.exe     C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\nb2pdf.exe      C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\open.exe        C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\strrep.exe      C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\svg2pdf.exe     C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\texclean.exe    C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\texini.exe      C:\PROJECTS\KARI\docs\bin\ /y
copy C:\home\bin\xlt.exe         C:\PROJECTS\KARI\docs\bin\ /y

copy C:\home\bin\autojosa.py    C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\bmind.py       C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\docbuild.py    C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\imginfo.py     C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\imgsize.py     C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\nb2pdf.py      C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\open.py        C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\strrep.py      C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\svg2pdf.py     C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\texclean.py    C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\texini.py      C:\PROJECTS\KARI\docs\bin\python\ /y
copy C:\home\bin\xlt.py         C:\PROJECTS\KARI\docs\bin\python\ /y
