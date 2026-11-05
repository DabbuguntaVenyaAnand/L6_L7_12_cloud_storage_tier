# Lab 7 - Fuzzing for Input Validation Bugs

Implemented against `Lab_7_FuzzTesting_Student_Handout.docx`.

## Required code deliverables

- `processor.py`: fixed application; invalid input returns `None` and the interactive CLI prints a clear message instead of crashing.
- `test_processor.py`: completed Hypothesis safety properties, valid-input properties, targeted regressions, input-length boundaries and command-line tests. No xfail or skip markers.
- `evidence/before/processor.py`: unchanged original application, preserved to reproduce the before-fix screenshots.
- `evidence/before/test_processor.py`: the same three core no-crash fuzz properties, exercised against the original application.

## Bugs and fixes

- None/non-string values caused AttributeError in string methods. Functions now check the type before string operations.
- Missing or nonnumeric quota amounts caused ValueError; unknown units caused KeyError. Quotas now require nonnegative ASCII digits followed by MB, GB or TB.
- Very large quota strings could overflow floating-point conversion. All functions reject inputs longer than 128 characters before parsing. The accepted quota length cannot overflow a float at the supported multipliers.
- Malformed ratio strings caused unpacking/conversion errors. Ratios now require exactly one colon and numeric components.
- Zero compressed size caused ZeroDivisionError. Compressed size must be positive; raw size must be nonnegative.
- NaN, infinity and an overflowing ratio could produce non-finite results. Inputs and results are now checked with `math.isfinite`.
- Missing/unknown tier prefixes caused KeyError. Supported HOT/COL/ARC prefixes use safe lookup; unknown values return None.
- EOF at the command-line prompt caused EOFError. The CLI now exits cleanly with a message.

Valid examples remain unchanged: 500MB becomes `Quota: 0.50 GB`; 1024:256 gives 4.0; HOT_TIER gives 0.08. Zero raw size is valid. Case normalization, surrounding whitespace, decimal quota units and the original tier-prefix convention are retained.

## Actual evidence

Final suite: **54 passed**, with no failures, skips or expected failures.

- Original application run with inputs `500MB`, `1:0`, `HOT_TIER` crashes with ZeroDivisionError before the third operation.
- Original application fails all three no-crash fuzz properties; minimized examples include None for quota/ratio and an empty string for the tier.
- Fixed application processes the same inputs without a traceback, prints an invalid-compression message and still returns the HOT rate.
- The seven Hypothesis properties each completed 300 passing generated examples (2,100 total in the recorded statistics run). Rejected generator draws are not application failures. Additional deterministic tests check concrete invalid and valid cases and CLI behavior.
- Actual outputs are in `evidence/buggy-application.txt`, `evidence/failing-tests.txt`, `evidence/fixed-application.txt`, `evidence/fixed-valid-application.txt` and `evidence/passing-tests.txt`.

## Four screenshots required by the handout

The code and text evidence are ready. **The PDF is pending the four genuine terminal screenshots.** Run each command from this folder and capture the visible output:

```powershell
powershell -NoProfile -File .\Show-Lab7.ps1 -Mode buggy-app
powershell -NoProfile -File .\Show-Lab7.ps1 -Mode failing-tests
powershell -NoProfile -File .\Show-Lab7.ps1 -Mode fixed-app
powershell -NoProfile -File .\Show-Lab7.ps1 -Mode passing-tests
```

Suggested image names in `evidence/`: `01-buggy-app.png`, `02-failing-tests.png`, `03-fixed-app.png`, `04-passing-tests.png`. The first two runs deliberately reproduce failures from the preserved original. They do not overwrite the fixed application.

After the images are supplied, include all four in `Lab7_FuzzTesting_Report.pdf`; do not substitute text logs or fabricated screenshots. The handout asks for the PDF, fixed application and updated tests.

## Reproduce tests

From `Lab 7/`:

```powershell
& ../.venv/Scripts/python.exe -m pytest test_processor.py -q --hypothesis-show-statistics
```

Windows / Python 3.12.14. Exact pytest and Hypothesis versions are in `requirements.txt`. The `pytest.ini` excludes archived before-fix evidence from normal recursive collection.
