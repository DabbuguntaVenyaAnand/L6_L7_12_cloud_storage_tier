"""Input-validation fuzz tests. Every supported input must return safely."""
import math
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st
from processor import parse_storage_quota, compute_compression_ratio, lookup_bandwidth_tier_rate

FUZZ = settings(max_examples=300, derandomize=True, deadline=None, report_multiple_bugs=False)
FUNCTIONS = (parse_storage_quota, compute_compression_ratio, lookup_bandwidth_tier_rate)


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


@FUZZ
@given(st.one_of(st.integers(), st.floats(), st.binary(), st.booleans(),
                st.lists(st.integers(), max_size=5), st.dictionaries(st.text(max_size=5), st.integers(), max_size=3)))
def test_nonstring_inputs_are_rejected_without_exceptions(value):
    for function in FUNCTIONS:
        assert no_crash(function, value) is None


@FUZZ
@given(amount=st.integers(min_value=0, max_value=10**9), unit=st.sampled_from(["MB", "GB", "TB"]),
       whitespace=st.sampled_from(["", " ", "\t", "\n"]))
def test_valid_quotas_preserve_conversion(amount, unit, whitespace):
    expected = amount * {"MB": .001, "GB": 1., "TB": 1000.}[unit]
    assert parse_storage_quota(f"{whitespace}{amount}{unit.lower()}{whitespace}") == f"Quota: {expected:.2f} GB"


@FUZZ
@given(raw=st.integers(min_value=0, max_value=10**9), compressed=st.integers(min_value=1, max_value=10**9))
def test_valid_ratios_preserve_calculation(raw, compressed):
    assert compute_compression_ratio(f"{raw}:{compressed}") == round(raw / compressed, 2)


@FUZZ
@given(tier=st.sampled_from([("HOT", .08), ("COLD", .05), ("ARCHIVE", .02)]),
       suffix=st.text(max_size=30), whitespace=st.sampled_from(["", " ", "\t"]))
def test_valid_tiers_preserve_case_insensitive_prefix_lookup(tier, suffix, whitespace):
    name, expected = tier
    assert lookup_bandwidth_tier_rate(whitespace + name.lower() + suffix) == expected


@pytest.mark.parametrize("value", [None, "", "GB", "1XX", "-1GB", "+1GB", "1.5GB", "NaNGB", "1e3GB", "9" * 400 + "GB", "1GB" + " " * 128])
def test_quota_invalid_regressions(value):
    assert parse_storage_quota(value) is None


@pytest.mark.parametrize("value", [None, "", "1", "1:2:3", "abc:2", "1:0", "1:-0", "-1:2", "1:-2", "nan:1", "1:nan", "inf:1", "1:inf", "1e308:1e-308", "1:2" + " " * 128])
def test_ratio_invalid_regressions(value):
    assert compute_compression_ratio(value) is None


@pytest.mark.parametrize("value", [None, "", "HO", "???", "UNKNOWN", "HOT" + "x" * 128])
def test_tier_invalid_regressions(value):
    assert lookup_bandwidth_tier_rate(value) is None


@pytest.mark.parametrize("value,expected", [("500MB", "Quota: 0.50 GB"), ("20GB", "Quota: 20.00 GB"), ("2TB", "Quota: 2000.00 GB"), ("0GB", "Quota: 0.00 GB")])
def test_quota_examples(value, expected):
    assert parse_storage_quota(value) == expected


@pytest.mark.parametrize("value,expected", [("1024:256", 4.0), ("0:1", 0.0), ("1:3", .33), ("1e3:2e2", 5.0)])
def test_ratio_examples(value, expected):
    assert compute_compression_ratio(value) == expected


@pytest.mark.parametrize("data,expected", [("500MB\n1024:256\nHOT_TIER\n", ["Quota: 0.50 GB", "Compression Ratio: 4.0", "0.08"]),
    ("1XX\n1:0\nUNKNOWN\n", ["Invalid quota", "Invalid compression", "Invalid tier"]),
    ("500MB\n1:0\nHOT_TIER\n", ["Quota: 0.50 GB", "Invalid compression", "0.08"])])
def test_command_line_continues_without_tracebacks(data, expected):
    result = subprocess.run([sys.executable, str(Path(__file__).with_name("processor.py"))], input=data, text=True, capture_output=True, timeout=10)
    assert result.returncode == 0
    assert "Traceback" not in result.stderr
    for message in expected:
        assert message in result.stdout


def test_command_line_eof_is_handled():
    result = subprocess.run([sys.executable, str(Path(__file__).with_name("processor.py"))], input="", text=True, capture_output=True, timeout=10)
    assert result.returncode == 0
    assert "Input ended" in result.stdout


@pytest.mark.parametrize("function,value,expected", [(parse_storage_quota, "1GB", "Quota: 1.00 GB"),
    (compute_compression_ratio, "1:2", .5), (lookup_bandwidth_tier_rate, "HOT", .08)])
def test_input_length_boundary(function, value, expected):
    assert function(value.ljust(128)) == expected
    assert function(value.ljust(129)) is None
