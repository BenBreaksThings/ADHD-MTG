Get-ChildItem -File | ForEach-Object {
	$oldName = $_.Name
	$newName = $oldName -replace '\(Token\)', '[T]'

	if ($newName -ne $oldName) {
		Rename-Item -LiteralPath $_.FullName -NewName $newName
	}
}
