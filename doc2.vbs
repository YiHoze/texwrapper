'd:\home\bin\d2d.vbs . %1 %2
'Const wdFormatDocument = 0
'Const wdFormatDocument97 = 0
'Const wdFormatDocumentDefault = 16
'Const wdFormatDOSText = 4
'Const wdFormatDOSTextLineBreaks = 5
'Const wdFormatEncodedText = 7
'Const wdFormatFilteredHTML = 10
'Const wdFormatFlatXML = 19
'Const wdFormatFlatXMLMacroEnabled = 20
'Const wdFormatFlatXMLTemplate = 21
'Const wdFormatFlatXMLTemplateMacroEnabled = 22
'Const wdFormatHTML = 8
'Const wdFormatPDF = 17
'Const wdFormatRTF = 6
'Const wdFormatTemplate = 1
'Const wdFormatTemplate97 = 1
'Const wdFormatText = 2
'Const wdFormatTextLineBreaks = 3
'Const wdFormatUnicodeText = 7
'Const wdFormatWebArchive = 9
'Const wdFormatXML = 11
'Const wdFormatXMLDocument = 12
'Const wdFormatXMLDocumentMacroEnabled = 13
'Const wdFormatXMLTemplate = 14
'Const wdFormatXMLTemplateMacroEnabled = 15
'Const wdFormatXPS = 18
'Const wdFormatOfficeDocumentTemplate = 23

Option Explicit 

Sub main()
Dim ArgCount
ArgCount = WScript.Arguments.Count
Select Case ArgCount 
	Case 3	
		Dim SrcFilePaths,objshell, SrcFileExtension, TrgFileExtension
		SrcFilePaths = WScript.Arguments(0)
		SrcFileExtension = WScript.Arguments(1)
		TrgFileExtension = WScript.Arguments(2)
		StopWordApp
		Set objshell = CreateObject("scripting.filesystemobject")
		If objshell.FolderExists(SrcFilePaths) Then  
			Dim flag,FileNumber
			flag = 0 
			FileNumber = 0 	
			Dim Folder,TrgFiles,TrgFile		
			Set Folder = objshell.GetFolder(SrcFilePaths)
			Set TrgFiles = Folder.Files
			For Each TrgFile In TrgFiles  
				FileNumber=FileNumber+1 
				SrcFilePath = TrgFile.Path
				If GetSrcFile(SrcFilePath, SrcFileExtension) Then  
					ConvertSrcToTrg SrcFilePath, TrgFileExtension
					flag=flag+1
				End If 	
			Next 
			WScript.Echo  flag & " files in the folder are converted."
		Else 
			If GetSrcFile(SrcFilePaths, SrcFileExtension) Then  
				Dim SrcFilePath
				SrcFilePath = SrcFilePaths				
				ConvertSrcToTrg SrcFilePath, TrgFileExtension
				WScript.Echo  SrcFilePath & " is successfully converted."
			End If  
		End If 			
	Case  Else 
	 	WScript.Echo "Usage: d2d.vbs path source-extension target-extension."
End Select 
End Sub 

Function GetFileType(FileType)
	Dim i, FileTypes(8,2)
	FileTypes(0,0) = "doc"
	FileTypes(0,1) = 0
	FileTypes(1,0) = "rtf"
	FileTypes(1,1) = 6
	FileTypes(2,0) = "txt"
	FileTypes(2,1) = 7
	FileTypes(3,0) = "tex"
	FileTypes(3,1) = 7
	FileTypes(4,0) = "html"
	FileTypes(4,1) = 8
	FileTypes(5,0) = "xml"
	FileTypes(5,1) = 11
	FileTypes(6,0) = "docx"
	FileTypes(6,1) = 16
	FileTypes(7,0) = "pdf"
	FileTypes(7,1) = 17
	For i=0 to UBound(FileTypes)
		If StrComp(FileType, FileTypes(i, 0), vbTextCompare) = 0 Then
			GetFileType = FileTypes(i, 1)
			Exit For
		End If
	Next
End Function

Function ConvertSrcToTrg(SrcFilePath, TrgFileExtension)
	Dim objshell, ParentFolder, BaseName, WordFilePath, wordapp, doc
	Set objshell= CreateObject("scripting.filesystemobject")
	ParentFolder = objshell.GetParentFolderName(SrcFilePath) 
	BaseName = objshell.GetBaseName(SrcFilePath) 
	WordFilePath = parentFolder & "\" & BaseName & "." & TrgFileExtension  
	Set wordapp = CreateObject("Word.Application")
	Set doc = wordapp.documents.open(SrcFilePath)
	doc.saveas WordFilePath, GetFileType(TrgFileExtension)
	doc.close
	wordapp.quit
	Set objshell = Nothing 
End Function 

Function GetSrcFile(SrcFilePath, SrcFileExtension) 
	Dim objshell
	Set objshell= CreateObject("scripting.filesystemobject")
	Dim Arrs ,Arr
	Arrs = Array(SrcFileExtension) 
	Dim blnIsTrgFile,FileExtension
	blnIsTrgFile= False 
	FileExtension = objshell.GetExtensionName(SrcFilePath)  
	For Each Arr In Arrs
		If InStr(UCase(FileExtension),UCase(Arr)) <> 0 Then 
			blnIsTrgFile= True
			Exit For 
		End If 
	Next 
	GetSrcFile = blnIsTrgFile
	Set objshell = Nothing 
End Function 

Function StopWordApp 
	Dim strComputer,objWMIService,colProcessList,objProcess 
	strComputer = "."
	Set objWMIService = GetObject("winmgmts:" _
		& "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
	Set colProcessList = objWMIService.ExecQuery _
		("SELECT * FROM Win32_Process WHERE Name = 'Winword.exe'")
	For Each objProcess in colProcessList
		objProcess.Terminate()
	Next
End Function 

Call main 
