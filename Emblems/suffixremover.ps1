$suffixes = 'Lan|Ins|Cre|Art|Enc|Pla|Bat|Sor|Tok|Emb|Leg'

Get-ChildItem -Path . -File -Recurse | ForEach-Object {
	$newName = $_.BaseName -replace "(\s*\[($suffixes)\])+$", ""
	$newName = $newName.TrimEnd() + $_.Extension

	if ($newName -ne $_.Name) {
		$destination = Join-Path $_.DirectoryName $newName

		if (Test-Path -LiteralPath $destination) {
			Write-Warning "SKIPPED (already exists): $destination"
		}
		else {
			Rename-Item -LiteralPath $_.FullName -NewName $newName
			Write-Host "RENAMED: $($_.Name) -> $newName"
		}
	}
}