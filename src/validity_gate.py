"""Matrix validity gate based on a Mahalanobis distance model."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

VALIDITY_LIMIT = 15.0

@dataclass(frozen=True)
class ValidityResult:
    valid: bool
    distance_squared: float
    reason: str

def mahalanobis_squared(features: np.ndarray, mean: np.ndarray, inverse_covariance: np.ndarray) -> float:
    x = np.asarray(features, dtype=float).reshape(-1)
    mu = np.asarray(mean, dtype=float).reshape(-1)
    inv = np.asarray(inverse_covariance, dtype=float)
    if x.shape != mu.shape or inv.shape != (x.size, x.size):
        raise ValueError("feature, mean and inverse covariance dimensions do not agree")
    delta = x - mu
    return float(delta @ inv @ delta)

def validate_matrix(features: np.ndarray, mean: np.ndarray, inverse_covariance: np.ndarray, limit: float = VALIDITY_LIMIT) -> ValidityResult:
    d2 = mahalanobis_squared(features, mean, inverse_covariance)
    valid = bool(d2 <= limit)
    return ValidityResult(valid=valid, distance_squared=d2, reason="VALID" if valid else "INVALID")
