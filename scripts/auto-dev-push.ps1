# ============================================
# AUTOMATIC DEV COMMIT + PUSH
# ============================================

$repo = "D:\OneDrive - Sri Lanka Telecom PLC\3. Trainings\AWS Cloud Associate\github\project-01\aws-training"

Set-Location $repo

Write-Host ""
Write-Host "========================================"
Write-Host " Git Auto Sync - DEV"
Write-Host "========================================"
Write-Host ""

# Make sure this is a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not a Git repository."
    exit 1
}

# Check current branch
$currentBranch = git branch --show-current

Write-Host "Current branch: $currentBranch"

# Only allow DEV
if ($currentBranch -ne "dev") {
    Write-Host "Switching to dev..."
    git switch dev

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Cannot switch to dev."
        exit 1
    }
}

# Check changes
$changes = git status --porcelain

if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "No local changes detected."
    exit 0
}

Write-Host "Changes detected."
Write-Host ""

git status --short

Write-Host ""
Write-Host "Staging changes..."

git add -A

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: git add failed."
    exit 1
}

# Commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "Creating commit..."

git commit -m "Auto update: $timestamp"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Commit failed."
    exit 1
}

# Get latest dev version
Write-Host "Checking remote dev branch..."

git pull --rebase origin dev

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Rebase conflict detected."
    Write-Host "Automatic push stopped."
    Write-Host ""

    git rebase --abort

    exit 1
}

# Push to DEV
Write-Host "Pushing to GitHub dev..."

git push origin dev

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: DEV updated."
}
else {
    Write-Host ""
    Write-Host "ERROR: Push failed."
    exit 1
}