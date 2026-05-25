from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_SYSTEM_PROMPT = (
    "You are taking a verifier-backed evaluation. Solve privately, but output only "
    "one XML tag in this exact form: <answer>FINAL</answer>. Do not include "
    "explanations, markdown, or any text outside the answer tag."
)


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_keys: tuple[str, ...]
    max_concurrency: int
    timeout_seconds: float
    retries: int
    max_tokens: int
    system_prompt: str
    deepseek_base_url: str
    deepseek_api_key: str


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_settings() -> Settings:
    load_dotenv()
    combined = os.getenv("NVIDIA_API_KEYS", "")
    numbered = [os.getenv("NVIDIA_API_KEY_1", ""), os.getenv("NVIDIA_API_KEY_2", "")]
    keys = [item.strip() for item in combined.split(",") if item.strip()]
    keys.extend(item.strip() for item in numbered if item and item.strip())

    return Settings(
        base_url=os.getenv("NVIDIA_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        api_keys=tuple(dict.fromkeys(keys)),
        max_concurrency=int(os.getenv("LIVEPROOF_MAX_CONCURRENCY", "2")),
        timeout_seconds=float(os.getenv("LIVEPROOF_TIMEOUT_SECONDS", "180")),
        retries=int(os.getenv("LIVEPROOF_RETRIES", "5")),
        max_tokens=int(os.getenv("LIVEPROOF_MAX_TOKENS", "160")),
        system_prompt=os.getenv("LIVEPROOF_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
        deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", DEFAULT_DEEPSEEK_BASE_URL).rstrip("/"),
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
    )
