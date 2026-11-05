param([ValidateSet('code','branch')][string]$Mode = 'code')
Set-Location -LiteralPath $PSScriptRoot
$labPython = Join-Path $PSScriptRoot '../.venv/Scripts/python.exe'
$Host.UI.RawUI.WindowTitle = "Lab 6 - $Mode coverage results"
Clear-Host
Write-Host 'LAB 6: CLOUD STORAGE TIER' -ForegroundColor Cyan
Write-Host "Mode: $Mode coverage | Application source unchanged"
Write-Host ''
if ($Mode -eq 'code') {
    Write-Host 'python -m coverage run --source=cloud_storage_tier -m pytest CodeCoverageTest_cloud_storage_tier.py -q'
    & $labPython -m coverage run --data-file=evidence/.coverage-code --source=cloud_storage_tier -m pytest CodeCoverageTest_cloud_storage_tier.py -q
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host ''
    Write-Host 'python -m coverage report -m --fail-under=90'
    & $labPython -m coverage report --data-file=evidence/.coverage-code -m --fail-under=90
} else {
    Write-Host 'python -m coverage run --branch --source=cloud_storage_tier -m pytest BranchCoverageTest_cloud_storage_tier.py -q'
    & $labPython -m coverage run --data-file=evidence/.coverage-branch --source=cloud_storage_tier --branch -m pytest BranchCoverageTest_cloud_storage_tier.py -q
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host ''
    Write-Host 'python -m coverage report -m --fail-under=90'
    & $labPython -m coverage report --data-file=evidence/.coverage-branch -m --fail-under=90
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ''
Write-Host 'Verified: coverage exceeds the required 90%.' -ForegroundColor Green
