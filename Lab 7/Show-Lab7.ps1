param([ValidateSet('buggy-app','failing-tests','fixed-app','passing-tests')][string]$Mode)
Set-Location -LiteralPath $PSScriptRoot
$labPython = Join-Path $PSScriptRoot '../.venv/Scripts/python.exe'
$Host.UI.RawUI.WindowTitle = "Lab 7 - $Mode"
Clear-Host
Write-Host 'LAB 7: FUZZING FOR INPUT VALIDATION BUGS' -ForegroundColor Cyan
Write-Host "Evidence: $Mode"
Write-Host ''
switch ($Mode) {
    'buggy-app' {
        Set-Location -LiteralPath (Join-Path $PSScriptRoot 'evidence/before')
        Write-Host 'BEFORE FIX: original processor.py'
        Write-Host 'Inputs supplied: 500MB, 1:0, HOT_TIER'
        Write-Host 'python processor.py'
        @('500MB', '1:0', 'HOT_TIER') | & $labPython processor.py
        Write-Host "Original application exit code: $LASTEXITCODE (crash expected)"
    }
    'failing-tests' {
        Set-Location -LiteralPath (Join-Path $PSScriptRoot 'evidence/before')
        Write-Host 'BEFORE FIX: three real Hypothesis safety properties'
        Write-Host 'python -m pytest test_processor.py -q --tb=line'
        & $labPython -m pytest test_processor.py -q --tb=line
        Write-Host "Original test exit code: $LASTEXITCODE (failures expected)"
    }
    'fixed-app' {
        Write-Host 'AFTER FIX: invalid ratio handled; remaining tier operation still executes'
        Write-Host 'Same inputs: 500MB, 1:0, HOT_TIER'
        Write-Host 'python processor.py'
        @('500MB', '1:0', 'HOT_TIER') | & $labPython processor.py
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        Write-Host 'Fixed application completed without a traceback.' -ForegroundColor Green
    }
    'passing-tests' {
        Write-Host 'AFTER FIX: safety properties, valid-input properties, regression and CLI tests'
        Write-Host 'python -m pytest test_processor.py -q'
        & $labPython -m pytest test_processor.py -q
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        Write-Host 'All tests pass; no skips or expected failures.' -ForegroundColor Green
    }
}
