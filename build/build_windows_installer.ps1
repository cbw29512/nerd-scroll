try {
    $ErrorActionPreference = "Stop"

    # -----------------------------
    # Objective:
    # Build a normal Windows installer for Nerd Scroll.
    #
    # State/Data outputs:
    # - dist/NerdScrollApp/NerdScroll.exe
    # - dist/NerdScrollApp/NerdScrollRunner.exe
    # - dist/NerdScrollApp/bundled_packs/*
    # - release/NerdScrollSetup-v0.9.0.exe
    # -----------------------------

    $RepoDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    $DistDir = Join-Path $RepoDir "dist"
    $StageDir = Join-Path $DistDir "NerdScrollApp"
    $ReleaseDir = Join-Path $RepoDir "release"
    $BuildDir = Join-Path $RepoDir "build\pyinstaller"
    $Iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

    Write-Host "Nerd Scroll installer build starting..." -ForegroundColor Cyan
    Write-Host "Repo: $RepoDir" -ForegroundColor DarkCyan

    Set-Location $RepoDir

    # -----------------------------
    # Validate required source files before doing work.
    # -----------------------------
    $RequiredPaths = @(
        ".\_nerd_scroll_app\packaged_gui_launcher.py",
        ".\_nerd_scroll_app\runner_cli.py",
        ".\_nerd_scroll_app\nerd_scroll\runner_process.py",
        ".\bundled_packs",
        ".\installer\NerdScroll.iss",
        ".\installer\desktop-workspace\README_FIRST.txt",
        ".\installer\desktop-workspace\Homemade Scrollers\README_PUT_HOMEMADE_SCROLLERS_HERE.txt",
        ".\installer\desktop-workspace\Purchased Scrollers\README_PUT_PURCHASED_SCROLLERS_HERE.txt",
        ".\requirements-build.txt"
    )

    foreach ($Path in $RequiredPaths) {
        if (-not (Test-Path $Path)) {
            throw "Missing required path: $Path. Run git pull origin main first."
        }
    }

    if (-not (Test-Path $Iscc)) {
        throw "Inno Setup compiler not found at $Iscc. Install Inno Setup 6, then run this again."
    }

    # -----------------------------
    # Install Python build dependencies.
    # -----------------------------
    python -m pip install -r .\requirements-build.txt
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed."
    }

    # -----------------------------
    # Clean build output.
    # -----------------------------
    Remove-Item $StageDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $DistDir "NerdScroll") -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $ReleaseDir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $StageDir | Out-Null
    New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

    # -----------------------------
    # Build GUI executable.
    # -----------------------------
    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onedir `
        --windowed `
        --name NerdScroll `
        --contents-directory . `
        --distpath $DistDir `
        --workpath $BuildDir `
        --paths .\_nerd_scroll_app `
        --collect-all tkinterdnd2 `
        .\_nerd_scroll_app\packaged_gui_launcher.py

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller GUI build failed."
    }

    Copy-Item (Join-Path $DistDir "NerdScroll\*") $StageDir -Recurse -Force

    # -----------------------------
    # Build terminal runner executable.
    # -----------------------------
    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --console `
        --name NerdScrollRunner `
        --distpath $StageDir `
        --workpath $BuildDir `
        --paths .\_nerd_scroll_app `
        .\_nerd_scroll_app\runner_cli.py

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller runner build failed."
    }

    # -----------------------------
    # Copy bundled starter packs into the staged app.
    # -----------------------------
    Copy-Item ".\bundled_packs" (Join-Path $StageDir "bundled_packs") -Recurse -Force

    @'
NERD SCROLL

Open Nerd Scroll from the Start Menu or Desktop shortcut.

How to use:
1. Choose a starter pack or add your own pack.
2. Click Load Pack.
3. Pick a speed.
4. Click START NERD SCROLL.

Stop by pressing Ctrl+C inside the terminal window or by closing it.

Nerd Scroll reads text only. It does not execute pack text.
'@ | Set-Content (Join-Path $StageDir "README_START_HERE.txt") -Encoding UTF8

    # -----------------------------
    # Build final installer EXE.
    # -----------------------------
    & $Iscc ".\installer\NerdScroll.iss"
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup build failed."
    }

    $Installer = Join-Path $ReleaseDir "NerdScrollSetup-v0.9.0.exe"
    if (-not (Test-Path $Installer)) {
        throw "Installer was not created: $Installer"
    }

    Write-Host "" 
    Write-Host "PASS: Installer created." -ForegroundColor Green
    Write-Host $Installer -ForegroundColor Cyan
}
catch {
    Write-Host "" 
    Write-Host "FAIL: Installer build stopped." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    exit 1
}
