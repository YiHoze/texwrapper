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
