import pytest
from hypothesis import given, settings, strategies as st
from processor import parse_storage_quota, compute_compression_ratio, lookup_bandwidth_tier_rate

FUZZ = settings(max_examples=300, derandomize=True, deadline=None, report_multiple_bugs=False)

def no_crash(function, value):
    try:
        return function(value)
    except Exception as error:
        pytest.fail(f"{function.__name__} crashed for {value!r}: {type(error).__name__}: {error}")


@FUZZ
@given(st.text() | st.none())
def test_parse_storage_quota_no_crash(value):
    result = no_crash(parse_storage_quota, value)
    assert result is None or (isinstance(result, str) and result.startswith("Quota: ") and result.endswith(" GB"))


@FUZZ
@given(st.text() | st.none())
def test_compute_compression_ratio_no_crash(value):
    result = no_crash(compute_compression_ratio, value)
    assert result is None or (isinstance(result, float) and math.isfinite(result) and result >= 0)


@FUZZ
@given(st.text() | st.none())
def test_lookup_bandwidth_tier_rate_no_crash(value):
    assert no_crash(lookup_bandwidth_tier_rate, value) in (None, .08, .05, .02)
