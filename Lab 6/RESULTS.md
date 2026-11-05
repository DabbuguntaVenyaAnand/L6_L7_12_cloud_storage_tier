# Lab 6 — handout submission checklist

Implemented using `Lab_6_Code&BranchCoverage_Student_Handout.docx`.

- Code-coverage tests: `CodeCoverageTest_cloud_storage_tier.py` — 7 passed, 100% line coverage.
- Branch-coverage tests: `BranchCoverageTest_cloud_storage_tier.py` — 41 passed, 100% line and branch coverage.
- Initial single-test baseline: 45.61% line coverage, 35.00% branch coverage; saved as text/JSON, without a screenshot.
- Separate analyses: `CODE_COVERAGE_ANALYSIS.md` and `BRANCH_COVERAGE_ANALYSIS.md`.
- Real command output and JSON evidence: `evidence/`.
- Original application and starter test: unchanged.
- Two local commits: code-coverage deliverables first, branch-coverage deliverables second. Lab 7 is excluded.
- Actual student-supplied terminal screenshots: `evidence/code-coverage-terminal.png` and `evidence/branch-coverage-terminal.png`, saved and committed separately by coverage type.
- **Local Lab 6 deliverables are complete. The commits have not been pushed.**

## Reproduce the screenshot results

Open PowerShell in this folder and run:

```powershell
powershell -NoProfile -File .\Show-Coverage.ps1 -Mode code
```

Capture the successful test summary and 100% line-coverage report. Save as `evidence/code-coverage-terminal.png`.

Then run:

```powershell
powershell -NoProfile -File .\Show-Coverage.ps1 -Mode branch
```

Capture the successful test summary and report showing 40 branches, zero partial branches and 100% coverage. Save as `evidence/branch-coverage-terminal.png`.

Both supplied screenshots show results above 90% and include the commands, successful tests and coverage reports. No baseline screenshot is included, following the handout.

The tests, analysis and screenshots have been committed locally, exceeding the minimum two commits required by the handout. Push the local commits when ready to submit.

## Environment

Windows, Python 3.12.14. To set up another machine, create a virtual environment in the repository root and install `Lab 6/requirements.txt`. The test commands run from `Lab 6/`; explicit filenames are needed because the handout's capitalized filenames do not match pytest's default discovery pattern.
