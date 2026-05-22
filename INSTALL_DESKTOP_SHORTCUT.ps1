try {
    $ErrorActionPreference = "Stop"

    $RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $Launcher = Join-Path $RepoDir "2_RUN_NERD_SCROLL.bat"
    $Desktop = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = Join-Path $Desktop "Nerd Scroll.lnk"

    if (-not (Test-Path $Launcher)) {
        throw "Launcher not found: $Launcher"
    }

    $Shell = New-Object -ComObject WScript.Shell
    $Shortcut = $Shell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $Launcher
    $Shortcut.WorkingDirectory = $RepoDir
    $Shortcut.Description = "Nerd Scroll"
    $Shortcut.Save()

    Write-Host "PASS: Desktop shortcut installed:" -ForegroundColor Green
    Write-Host $ShortcutPath -ForegroundColor Cyan
}
catch {
    Write-Host "FAIL: Could not install desktop shortcut." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}
