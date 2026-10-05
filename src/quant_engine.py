"""4-parameter logistic quantitation and M-1 decision bands."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit

CUTOFF_UG_KG = 0.50
RETEST_LOW_UG_KG = 0.42
RETEST_HIGH_UG_KG = 0.58

def four_parameter_logistic(x: np.ndarray | float, top: float, bottom: float, ec50: float, slope: float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if np.any(x <= 0):
        raise ValueError("4PL concentration must be positive")
    if ec50 <= 0:
        raise ValueError("ec50 must be positive")
    return bottom + (top - bottom) / (1.0 + (x / ec50) ** slope)

@dataclass(frozen=True)
class FourPLFit:
    top: float
    bottom: float
    ec50: float
    slope: float
    def predict_ratio(self, concentration_ug_kg: float | np.ndarray) -> np.ndarray:
        return four_parameter_logistic(concentration_ug_kg, self.top, self.bottom, self.ec50, self.slope)

def fit_4pl(concentration_ug_kg: np.ndarray, response: np.ndarray) -> FourPLFit:
    x = np.asarray(concentration_ug_kg, dtype=float)
    y = np.asarray(response, dtype=float)
    if x.shape != y.shape or x.size < 4:
        raise ValueError("at least four paired calibration points are required")
    order = np.argsort(x)
    x, y = x[order], y[order]
    p0 = [float(np.max(y)), float(np.min(y)), float(np.median(x)), 1.0]
    bounds = ([0.0, -1.0, 1e-9, 0.05], [2.0, 2.0, np.inf, 10.0])
    params, _ = curve_fit(four_parameter_logistic, x, y, p0=p0, bounds=bounds, maxfev=20000)
    return FourPLFit(*map(float, params))

def classify_concentration(concentration_ug_kg: float) -> str:
    c = float(concentration_ug_kg)
    if c < RETEST_LOW_UG_KG:
        return "PASS"
    if c <= RETEST_HIGH_UG_KG:
        return "RETEST"
    return "SUSPECT"

def concentration_from_ratio(fit: FourPLFit, ratio: float, *, bounds=(1e-6, 100.0)) -> float:
    from scipy.optimize import brentq
    r = float(ratio)
    if not np.isfinite(r):
        raise ValueError("ratio must be finite")
    lo, hi = map(float, bounds)
    if lo <= 0 or hi <= lo:
        raise ValueError("invalid concentration bounds")
    f = lambda x: float(fit.predict_ratio(x)) - r
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        raise ValueError("ratio is outside the fitted concentration range")
    return float(brentq(f, lo, hi))
