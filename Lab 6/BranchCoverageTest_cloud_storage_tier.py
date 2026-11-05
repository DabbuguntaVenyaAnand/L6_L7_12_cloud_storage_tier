"""Boundary and branch coverage tests for the unmodified Lab 6 module."""
import pytest
from cloud_storage_tier import process_storage_tenants, monitor_replication_latency


def tenant(buckets=(), **fields):
    return {"account_active": True, "buckets": list(buckets), **fields}


@pytest.mark.parametrize("tenants,fee", [(None, 0), ({}, 0), ([], -1)])
def test_invalid_arguments(tenants, fee):
    with pytest.raises(ValueError):
        process_storage_tenants(tenants, fee)


@pytest.mark.parametrize("tenants", [[], [{}], [tenant(account_active=False)], [tenant()], [tenant([{}])]])
def test_zero_usage(tenants):
    assert process_storage_tenants(tenants, 10) == {"total_billed": 0.0, "status": "ZERO_USAGE"}


@pytest.mark.parametrize("tier,size,expected", [
    ("hot", 100, 2.5), ("cool", 100, 1.5), ("archive", 100, .5),
    ("hot", 500, 12.5), ("hot", 501, 11.27), ("cool", 600, 8.1), ("archive", 600, 2.7)])
def test_rates_and_discount_boundary(tier, size, expected):
    assert process_storage_tenants([tenant([{"size_gb": size}], tier=tier)], 0) == {"total_billed": expected, "status": "BILLED"}


def test_default_hot_tier():
    assert process_storage_tenants([tenant([{"size_gb": 100}])], 0)["total_billed"] == 2.5


@pytest.mark.parametrize("egress,expected", [(0, 2.5), (100, 2.5), (101, 2.58), (150, 6.5)])
def test_egress_boundary(egress, expected):
    assert process_storage_tenants([tenant([{"size_gb": 100, "egress_gb": egress}])], 0)["total_billed"] == expected


def test_invalid_bucket_skips_egress_and_continues():
    buckets = [{"size_gb": 0, "egress_gb": 500}, {"size_gb": -1}, {"size_gb": 100}]
    assert process_storage_tenants([tenant(buckets)], 0)["total_billed"] == 2.5


@pytest.mark.parametrize("tier,expected", [("hot", 6.5), ("cool", 5.5)])
def test_corrupted_nonarchive_still_charges_egress(tier, expected):
    buckets = [{"size_gb": 100, "corrupted": True, "egress_gb": 150}, {"size_gb": 100}]
    assert process_storage_tenants([tenant(buckets, tier=tier)], 0)["total_billed"] == expected


@pytest.mark.parametrize("backup,expected,status", [(False, 0, "ZERO_USAGE"), (True, 10, "BILLED")])
def test_archive_corruption_resets_charge_and_breaks_but_support_fee_remains(backup, expected, status):
    buckets = [{"size_gb": 100}, {"size_gb": 10, "corrupted": True, "egress_gb": 999}, {"size_gb": 900}]
    assert process_storage_tenants([tenant(buckets, tier="archive", has_backup_vault=backup)], 10) == {"total_billed": expected, "status": status}


def test_support_fee_per_active_known_tier():
    tenants = [tenant(has_backup_vault=True), tenant(has_backup_vault=True),
               tenant(account_active=False, has_backup_vault=True), tenant(tier="unknown", has_backup_vault=True)]
    assert process_storage_tenants(tenants, 7) == {"total_billed": 14.0, "status": "BILLED"}


@pytest.mark.parametrize("count,status", [(4, "ZERO_USAGE"), (5, "AUDIT_FLAGGED")])
def test_audit_boundary_and_zero_usage_precedence(count, status):
    assert process_storage_tenants([tenant([{"size_gb": 0}] * count)], 0) == {"total_billed": 0.0, "status": status}


def test_unknown_tiers_count_toward_audit_and_valid_charge_is_preserved():
    assert process_storage_tenants([tenant(tier="invalid")] * 5 + [tenant([{"size_gb": 100}])], 0) == {"total_billed": 2.5, "status": "AUDIT_FLAGGED"}


def test_corruption_counts_toward_audit_and_rounding_is_after_sum():
    tenants = [tenant([{"size_gb": 1, "corrupted": True}] * 5), tenant([{"size_gb": 1}] * 2)]
    assert process_storage_tenants(tenants, 0) == {"total_billed": .05, "status": "AUDIT_FLAGGED"}


@pytest.mark.parametrize("matrix,expected", [
    (None, "NO_DATA"), ([], "NO_DATA"), ([[]], "SYNCED"), ([[200]], "SYNCED"),
    ([[201]], "SYNCED"), ([[201, 201]], "SYNC_LAG_ALERT"), ([[201, 200, 201]], "SYNCED"),
    ([[201], [201]], "SYNCED"), ([[], [50, 201, 202]], "SYNC_LAG_ALERT"),
    ([[201, 0, 201, 201]], "SYNC_LAG_ALERT"), ([[0, 100], [199, 200]], "SYNCED")])
def test_replication_latency(matrix, expected):
    assert monitor_replication_latency(matrix) == expected
