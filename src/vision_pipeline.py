"""Deterministic optical preprocessing for the M-1 reader.

The functions here are deliberately hardware-agnostic so the same pipeline can run
on a desktop during development and on the Raspberry Pi Zero 2 W reader later.
"""
from __future__ import annotations

from dataclasses import dataclass
import cv2
import numpy as np


@dataclass(frozen=True)
class LabMeasurement:
    corrected_lab: np.ndarray
    delta_e: np.ndarray
    blank_lab: np.ndarray


def perspective_unwarp(image: np.ndarray, src_points: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Unwarp a card from four ordered corners using a projective transform."""
    pts = np.asarray(src_points, dtype=np.float32).reshape(4, 2)
    if image is None or image.size == 0:
        raise ValueError("image must be a non-empty array")
    if not np.isfinite(pts).all():
        raise ValueError("corner coordinates must be finite")
    w, h = map(int, output_size)
    if w <= 1 or h <= 1:
        raise ValueError("output_size must be greater than 1x1")
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(pts, dst)
    return cv2.warpPerspective(image, matrix, (w, h), flags=cv2.INTER_LINEAR)


def bgr_to_lab(image: np.ndarray) -> np.ndarray:
    """Convert an 8-bit BGR image to CIELAB."""
    if image is None or image.size == 0:
        raise ValueError("image must be non-empty")
    if image.dtype != np.uint8:
        image = np.clip(image, 0, 255).astype(np.uint8)
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)


def lab_to_float(lab: np.ndarray) -> np.ndarray:
    """Convert OpenCV 8-bit Lab to conventional L*,a*,b* units."""
    arr = np.asarray(lab, dtype=np.float32)
    out = arr.copy()
    out[..., 0] = out[..., 0] * (100.0 / 255.0)
    out[..., 1:] -= 128.0
    return out


def delta_e76(lab_a: np.ndarray, lab_b: np.ndarray) -> np.ndarray:
    """CIE76 colour difference between two Lab arrays or a Lab array and one colour."""
    a = lab_to_float(lab_a)
    b = lab_to_float(lab_b)
    return np.linalg.norm(a - b, axis=-1)


def optical_blank_reference_subtraction(lab_image: np.ndarray, blank_lab: np.ndarray | tuple[float, float, float]) -> np.ndarray:
    """Return ΔE76 from an optical blank/reference."""
    lab = lab_to_float(lab_image)
    blank = np.asarray(blank_lab, dtype=np.float32).reshape(3)
    return np.linalg.norm(lab - blank, axis=-1)


def measure_against_blank(image_bgr: np.ndarray, blank_bgr: np.ndarray) -> LabMeasurement:
    """Convert an image and blank to Lab and compute the differential ΔE field."""
    image_lab = bgr_to_lab(image_bgr)
    blank_lab = bgr_to_lab(blank_bgr)
    blank_mean = np.mean(lab_to_float(blank_lab).reshape(-1, 3), axis=0)
    de = optical_blank_reference_subtraction(image_lab, blank_mean)
    return LabMeasurement(corrected_lab=lab_to_float(image_lab), delta_e=de, blank_lab=blank_mean)
