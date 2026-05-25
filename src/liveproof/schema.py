from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Task:
    id: str
    family: str
    seed: str
    prompt: str
    verifier: dict[str, Any]
    answer: str

    def public_record(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "family": self.family,
            "seed": self.seed,
            "prompt": self.prompt,
            "verifier_hash": stable_hash(self.verifier),
        }
        payload["task_hash"] = stable_hash(payload)
        return payload

    def private_record(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["task_hash"] = stable_hash(self.public_record())
        return payload


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

