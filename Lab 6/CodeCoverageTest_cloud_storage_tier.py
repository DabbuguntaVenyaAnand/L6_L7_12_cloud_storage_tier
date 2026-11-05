"""Statement-focused scenarios for Lab 6; run this file explicitly."""
import pytest
from cloud_storage_tier import process_storage_tenants, monitor_replication_latency


def active(tier="hot", buckets=(), **extra):
    return {"account_active": True, "tier": tier, "buckets": list(buckets), **extra}


def test_invalid_input():
    with pytest.raises(ValueError):
        process_storage_tenants(None, 0)


def test_tenant_and_bucket_processing_lines():
    tenants = [
        {"account_active": False},
        active("invalid"),
        active("hot", [{"size_gb": 0}, {"size_gb": 100}, {"size_gb": 600, "egress_gb": 150}, {"size_gb": 1, "corrupted": True}]),
        active("cool", [{"size_gb": 100}]),
        active("archive", [{"size_gb": 100}, {"size_gb": 1, "corrupted": True}], has_backup_vault=True),
    ]
    # Hot: 2.50 + 13.50 + 4.00; cool: 1.50; archive: reset + support 10.
    assert process_storage_tenants(tenants, 10) == {"total_billed": 31.5, "status": "BILLED"}


def test_audit_return():
    assert process_storage_tenants([active("invalid")] * 5, 0) == {"total_billed": 0, "status": "AUDIT_FLAGGED"}


def test_zero_usage_return():
    assert process_storage_tenants([], 0) == {"total_billed": 0, "status": "ZERO_USAGE"}


def test_replication_no_data():
    assert monitor_replication_latency([]) == "NO_DATA"


def test_replication_alert_after_reset():
    assert monitor_replication_latency([[201, 0, 201, 202]]) == "SYNC_LAG_ALERT"


def test_replication_synced():
    assert monitor_replication_latency([[100, 201], []]) == "SYNCED"
