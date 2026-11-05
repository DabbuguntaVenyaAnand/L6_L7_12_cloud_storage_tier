# Lab 6: branch coverage analysis

`BranchCoverageTest_cloud_storage_tier.py` runs 41 tests against the unchanged application.

Measured result: **41 passed; 57/57 statements; 40/40 branch exits; zero partial branches; 100% line and 100% branch coverage**. The initial single test covered only 14/40 exits (35%).

## Decisions and boundaries

- Invalid tenant container and negative support fee are rejected independently.
- Active/inactive and empty/nonempty tenant and bucket loops are exercised.
- Hot, cool, archive and unsupported tiers are covered.
- Missing, zero, negative and positive sizes cover skipping and continued processing.
- Exactly 500 GB does not receive the discount; 501 GB does.
- Exactly 100 GB egress is free; 101 GB incurs an excess charge.
- Hot/cool corruption follows the no-storage-charge path while retaining egress billing.
- Archive corruption resets previous bucket charges and breaks the bucket loop; backup fees can still be added afterward.
- Backup enabled/disabled paths and repeated per-tenant fees are checked.
- Four flags do not trigger an audit; five do. Audit takes precedence over ZERO_USAGE and preserves valid billing.
- Replication tests cover no data, empty node logs, 200/201 ms, one/two consecutive high values, streak reset, and isolation between nodes.

These tests characterize the supplied rules; questionable business rules were not silently rewritten to increase coverage.

## Reproduce

From `Lab 6/`:

```powershell
& ../.venv/Scripts/python.exe -m coverage run --branch --source=cloud_storage_tier -m pytest BranchCoverageTest_cloud_storage_tier.py -q
& ../.venv/Scripts/python.exe -m coverage report -m --fail-under=90
```

Alternatively run `powershell -NoProfile -File .\Show-Coverage.ps1 -Mode branch`.

Measured logs and JSON metrics are in `evidence/branch-tests.txt`, `evidence/branch-coverage.txt`, and `evidence/branch-coverage.json`.

**Terminal screenshot:** [branch-coverage-terminal.png](evidence/branch-coverage-terminal.png), supplied by the student. It shows 41 passing tests, 40 branch exits, zero partial branches and 100% coverage.

100% branch coverage does not mean 100% path coverage. Loop counts, combinations of decisions, and data values create many additional paths. Function coverage is 2/2 application functions, invoked directly by the tests; this was established by inspection rather than a separate function-coverage tool.
