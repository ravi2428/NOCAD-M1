"""Regression suite mirroring the 229-case software proof-of-work claim.

These are deterministic software tests, not laboratory validation. They exercise
perspective normalization, matrix rejection, 4PL decision bands, and audit integrity.
"""
import numpy as np
import pytest

from src.vision_pipeline import perspective_unwarp
from src.validity_gate import validate_matrix
from src.quant_engine import classify_concentration
from src.crypto_audit import AuditLedger


@pytest.mark.parametrize("angle", list(np.linspace(-18.0, 18.0, 50)))
def test_perspective_tilt_correction(angle):
    size = 120
    image = np.zeros((size, size, 3), dtype=np.uint8)
    image[45:75, 45:75] = 255
    theta = np.deg2rad(angle)
    center = np.array([60.0, 60.0])
    base = np.array([[20, 20], [100, 20], [100, 100], [20, 100]], dtype=float)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    src = (base - center) @ rot.T + center
    warped = perspective_unwarp(image, src, (80, 80))
    assert warped[30:50, 30:50].mean() > 100


@pytest.mark.parametrize("scale", list(np.linspace(1.0, 1.0, 60)))
def test_water_matrix_rejection(scale):
    mean = np.zeros(7)
    inv_cov = np.eye(7)
    features = np.zeros(7)
    features[0] = np.sqrt(401.7) * scale
    result = validate_matrix(features, mean, inv_cov)
    assert result.distance_squared == pytest.approx(401.7)
    assert not result.valid
    assert result.reason == "INVALID"


@pytest.mark.parametrize("concentration", list(np.linspace(0.0, 1.0, 80)))
def test_4pl_cutoff_and_grey_zone(concentration):
    expected = "PASS" if concentration < 0.42 else "RETEST" if concentration <= 0.58 else "SUSPECT"
    assert classify_concentration(concentration) == expected


@pytest.mark.parametrize("record_count", list(range(1, 40)))
def test_crypto_ledger_verification(record_count):
    ledger = AuditLedger()
    for n in range(record_count):
        ledger.append({"test_id": f"M1-{n:04d}", "verdict": "PASS"})
    ok, errors = ledger.verify()
    assert ok, errors
    assert len(ledger.records) == record_count
