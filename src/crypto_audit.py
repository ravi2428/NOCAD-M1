"""Tamper-evident audit ledger using SHA-256 chaining and Ed25519 signatures."""
from __future__ import annotations
from dataclasses import dataclass
import base64
import hashlib
import json
from typing import Any
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@dataclass(frozen=True)
class SignedRecord:
    sequence: int
    previous_hash: str
    content_hash: str
    signature_b64: str
    payload: dict[str, Any]

class AuditLedger:
    def __init__(self, private_key: Ed25519PrivateKey | None = None):
        self.private_key = private_key or Ed25519PrivateKey.generate()
        self.records: list[SignedRecord] = []

    @property
    def public_key(self) -> Ed25519PublicKey:
        return self.private_key.public_key()

    def append(self, payload: dict[str, Any]) -> SignedRecord:
        sequence = len(self.records) + 1
        previous_hash = self.records[-1].content_hash if self.records else "0" * 64
        body = {"sequence": sequence, "previous_hash": previous_hash, "payload": payload}
        content_hash = sha256_hex(canonical_json(body))
        signature = self.private_key.sign(content_hash.encode("ascii"))
        record = SignedRecord(sequence, previous_hash, content_hash, base64.b64encode(signature).decode("ascii"), payload)
        self.records.append(record)
        return record

    def verify(self, public_key: Ed25519PublicKey | None = None) -> tuple[bool, list[str]]:
        key = public_key or self.public_key
        errors: list[str] = []
        previous = "0" * 64
        for expected_seq, record in enumerate(self.records, 1):
            if record.sequence != expected_seq:
                errors.append(f"sequence mismatch at record {record.sequence}")
            if record.previous_hash != previous:
                errors.append(f"chain link broken at record {record.sequence}")
            body = {"sequence": record.sequence, "previous_hash": record.previous_hash, "payload": record.payload}
            expected_hash = sha256_hex(canonical_json(body))
            if expected_hash != record.content_hash:
                errors.append(f"content hash mismatch at record {record.sequence}")
            try:
                key.verify(base64.b64decode(record.signature_b64), record.content_hash.encode("ascii"))
            except Exception:
                errors.append(f"signature mismatch at record {record.sequence}")
            previous = record.content_hash
        return (not errors, errors)
