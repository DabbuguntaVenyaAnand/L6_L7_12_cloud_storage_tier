"""Storage helpers hardened for Lab 7.

Invalid inputs return None; valid inputs retain the starter's result formats.
The CLI turns None into a clear message and continues to the next operation.
"""
import math
import re

MAX_INPUT_LENGTH = 128
_QUOTA = re.compile(r"([0-9]+)(MB|GB|TB)")


def _clean_text(value):
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip()


def parse_storage_quota(quota_str):
    """Convert nonnegative integer MB/GB/TB amounts to GB, or return None.

    Decimal units match the original: 1000 MB = 1 GB; 1 TB = 1000 GB.
    Input length is bounded before conversion to prevent excessive processing.
    """
    cleaned = _clean_text(quota_str)
    if not cleaned:
        return None
    match = _QUOTA.fullmatch(cleaned.upper())
    if match is None:
        return None
    amount, unit = match.groups()
    total = int(amount) * {"MB": .001, "GB": 1., "TB": 1000.}[unit]
    return f"Quota: {total:.2f} GB"


def compute_compression_ratio(size_metric_str):
    """Return rounded raw/compressed ratio, or None for invalid/nonfinite data."""
    cleaned = _clean_text(size_metric_str)
    if not cleaned or cleaned.count(":") != 1:
        return None
    raw_text, compressed_text = cleaned.split(":")
    try:
        raw = float(raw_text)
        compressed = float(compressed_text)
    except ValueError:
        return None
    if not math.isfinite(raw) or not math.isfinite(compressed) or raw < 0 or compressed <= 0:
        return None
    ratio = raw / compressed
    if not math.isfinite(ratio):
        return None
    return round(ratio, 2)


def lookup_bandwidth_tier_rate(tier_descriptor):
    """Return a supported tier-prefix rate, or None for unsupported input."""
    cleaned = _clean_text(tier_descriptor)
    if not cleaned:
        return None
    return {"HOT": .08, "COL": .05, "ARC": .02}.get(cleaned.upper()[:3])


def main():
    try:
        print("==== Running parse_storage_quota ====")
        value = parse_storage_quota(input("Enter quota (e.g. 500MB, 10GB, 2TB): "))
        print(value if value is not None else "Invalid quota: use nonnegative digits followed by MB, GB or TB (maximum 128 characters).")

        print("\n==== Running compute_compression_ratio ====")
        value = compute_compression_ratio(input("Enter raw:compressed bytes (e.g. 1024:256): "))
        if value is None:
            print("Invalid compression input: use finite raw >= 0 and compressed > 0, separated by one colon.")
        else:
            print("Compression Ratio:", value)

        print("\n==== Running lookup_bandwidth_tier_rate ====")
        value = lookup_bandwidth_tier_rate(input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): "))
        if value is None:
            print("Invalid tier: use a HOT, COL or ARC prefix (maximum 128 characters).")
        else:
            print("Rate per GB: $", value)
    except EOFError:
        print("Input ended. Run the application again to enter all three values.")


if __name__ == "__main__":
    main()
