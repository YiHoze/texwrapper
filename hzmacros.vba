Attribute VB_Name = "Module1"
Sub SortSheets()
Dim i As Integer
Dim j As Integer
Dim iAnswer As VbMsgBoxResult
'
' Prompt the user as which direction they wish to
' sort the worksheets.
'
   iAnswer = MsgBox("Sort Sheets in Ascending Order?" & Chr(10) _
     & "Clicking No will sort in Descending Order", _
     vbYesNoCancel + vbQuestion + vbDefaultButton1, "Sort Worksheets")
   For i = 1 To Sheets.Count
      For j = 1 To Sheets.Count - 1
'
' If the answer is Yes, then sort in ascending order.
'
         If iAnswer = vbYes Then
            If UCase$(Sheets(j).Name) > UCase$(Sheets(j + 1).Name) Then
               Sheets(j).Move After:=Sheets(j + 1)
            End If
'
' If the answer is No, then sort in descending order.
'
         ElseIf iAnswer = vbNo Then
            If UCase$(Sheets(j).Name) < UCase$(Sheets(j + 1).Name) Then
               Sheets(j).Move After:=Sheets(j + 1)
            End If
         End If
      Next j
   Next i
End Sub

Sub HyperlinkSheets()
    For Each c In Selection
      c.Hyperlinks.Add Anchor:=c, Address:="#'" & c.Value & "'!A1"
    Next c
End Sub

Public Sub GetSheetNames()
'Columns(1).Insert
    For i = 1 To Sheets.Count
        Cells(i, 1) = Sheets(i).Name
    Next i
End Sub

Public Sub GetSheetValues()
    For i = 2 To Sheets.Count
        'Cells(i, 1) = Sheets(i).Name
        Cells(i, 2) = Sheets(i).Cells(14, 1)
        Cells(i, 3) = Sheets(i).Cells(9, 1)
        Cells(i, 4) = Sheets(i).Cells(10, 1)
        Cells(i, 6) = Sheets(i).Cells(11, 1)
        Cells(i, 7) = Sheets(i).Cells(10, 1)
        Cells(i, 11) = Sheets(i).Cells(32, 7)
        Cells(i, 12) = Sheets(i).Cells(30, 1)
    Next i
End Sub

Public Sub SaveColumnsAsSeparateText()
Dim Sheet As Worksheet: Set Sheet = ThisWorkbook.Worksheets("Sheet1")
Dim Column As Integer
Dim Row As Integer
Dim stream
Set stream = CreateObject("ADODB.Stream")
stream.Charset = "utf-8"
Dim Path As String: Path = "c:\temp\"
Dim Name As String
Dim Filename As String
For Column = 2 To 18
    stream.Open
    For Row = 2 To Sheet.Cells(Sheet.Rows.Count, Column).End(xlUp).Row
        stream.WriteText Sheet.Cells(Row, Column).Value2, 1
    Next Row
    Name = Sheet.Cells(1, Column).Value2
    Filename = Path & Name & ".tex"
    stream.SaveToFile Filename, 2
    stream.Close
Next Column
End Sub


출처: http://hoze.tistory.com/1488 [Hoze]