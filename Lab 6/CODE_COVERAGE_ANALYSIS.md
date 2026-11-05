# Lab 6: code coverage analysis

The supplied single test passed but executed only 26 of 57 application statements (45.61%). The initial branch-enabled report also found only 14 of 40 branch exits (35.00%); coverage.py's combined statement/branch figure was 41.24%. These metrics are different and must not be confused.

`CodeCoverageTest_cloud_storage_tier.py` adds seven statement-focused tests. They cover validation failure; active/inactive tenants; all storage tiers and unknown tiers; invalid and corrupted buckets; discount and egress calculations; archive reset/break behavior; support fees; every billing status; and both replication outcomes plus missing data.

Measured result: **7 passed; 57/57 statements; 100% line coverage**. Source code was not modified. Actual command output and JSON metrics are in `evidence/code-tests.txt`, `evidence/code-coverage.txt`, and `evidence/code-coverage.json`. Baseline evidence is saved separately, without a baseline screenshot, as the handout requests screenshots only after reaching 90%.

From `Lab 6/`, run:

```powershell
& ../.venv/Scripts/python.exe -m coverage run --source=cloud_storage_tier -m pytest CodeCoverageTest_cloud_storage_tier.py -q
& ../.venv/Scripts/python.exe -m coverage report -m --fail-under=90
```

Alternatively run `powershell -NoProfile -File .\Show-Coverage.ps1 -Mode code`.

**Terminal screenshot:** [code-coverage-terminal.png](evidence/code-coverage-terminal.png), supplied by the student. It shows the successful 7-test run and 100% line-coverage report.

Line coverage records executed statements. It does not prove that every branch or every possible path was exercised. Branch coverage is measured independently in the second deliverable.
