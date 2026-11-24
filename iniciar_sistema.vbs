Set WshShell = CreateObject("WScript.Shell")
' El parámetro 0 oculta la ventana negra por completo
WshShell.Run chr(34) & WshShell.CurrentDirectory & "\lanzador_seguro.bat" & chr(34), 0, False
Set WshShell = Nothing
