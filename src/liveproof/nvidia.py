from __future__ import annotations

import asyncio
from dataclasses import dataclass
from itertools import cycle
from typing import Iterable

import httpx


@dataclass(frozen=True)
class Completion:
    text: str
    raw: dict


class NvidiaClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_keys: Iterable[str],
        timeout_seconds: float,
        max_concurrency: int,
        retries: int,
        max_tokens: int,
        system_prompt: str,
    ) -> None:
        keys = tuple(api_keys)
        if not keys:
            raise ValueError("No NVIDIA API keys configured.")
        self.base_url = base_url.rstrip("/")
        self._keys = cycle(keys)
        self._key_lock = asyncio.Lock()
        self._client = httpx.AsyncClient(timeout=timeout_seconds)
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._retries = retries
        self._max_tokens = max_tokens
        self._system_prompt = system_prompt

    async def close(self) -> None:
        await self._client.aclose()

    async def _next_key(self) -> str:
        async with self._key_lock:
            return next(self._keys)

    async def list_models(self) -> list[str]:
        key = await self._next_key()
        response = await self._client.get(
            f"{self.base_url}/models",
            headers={"Authorization": f"Bearer {key}"},
        )
        response.raise_for_status()
        data = response.json()
        models = data.get("data", data if isinstance(data, list) else [])
        return sorted(dict.fromkeys(str(item.get("id", item)) for item in models))

    async def chat(self, *, model: str, prompt: str) -> Completion:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": self._max_tokens,
        }
        raw = await self._post_json("/chat/completions", payload)
        message = raw["choices"][0].get("message", {})
        return Completion(text=message.get("content") or "", raw=_compact_raw(raw))

    async def _post_json(self, path: str, payload: dict) -> dict:
        last_error: Exception | None = None
        for attempt in range(self._retries + 1):
            try:
                async with self._semaphore:
                    key = await self._next_key()
                    response = await self._client.post(
                        f"{self.base_url}{path}",
                        headers={
                            "Authorization": f"Bearer {key}",
                            "Content-Type": "application/json",
                        },
                        json=payload,
                    )
                if response.status_code in {429, 500, 502, 503, 504} and attempt < self._retries:
                    await asyncio.sleep(min(60, 2 ** attempt))
                    continue
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPError, KeyError, IndexError) as exc:
                last_error = exc
                if isinstance(exc, httpx.HTTPStatusError):
                    status = exc.response.status_code
                    if 400 <= status < 500 and status != 429:
                        break
                if attempt >= self._retries:
                    break
                await asyncio.sleep(min(60, 2 ** attempt))
        raise RuntimeError(f"NVIDIA API call failed after {self._retries + 1} attempts: {last_error}")


def _compact_raw(raw: dict) -> dict:
    choice = raw.get("choices", [{}])[0] if isinstance(raw.get("choices"), list) else {}
    return {
        "id": raw.get("id"),
        "created": raw.get("created"),
        "finish_reason": choice.get("finish_reason"),
        "usage": raw.get("usage", {}),
    }
