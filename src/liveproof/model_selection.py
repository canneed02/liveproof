from __future__ import annotations

from dataclasses import dataclass


PRIORITY_MODELS = (
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "deepseek-reasoner",
    "deepseek-chat",
    "nvidia/nemotron-3-super-120b-a12b",
    "qwen/qwen3-coder-480b-a35b-instruct",
    "meta/llama-4-maverick-17b-128e-instruct",
    "openai/gpt-oss-120b",
    "deepseek-ai/deepseek-v4-flash",
    "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "mistralai/mistral-large-3-675b-instruct-2512",
    "moonshotai/kimi-k2.6",
    "deepseek-ai/deepseek-v4-pro",
)


@dataclass(frozen=True)
class ModelChoice:
    id: str
    reason: str


def select_models(available: list[str], limit: int = 5) -> tuple[ModelChoice, ...]:
    seen = set()
    choices: list[ModelChoice] = []
    available_set = set(available)
    for model_id in PRIORITY_MODELS:
        if model_id in available_set and model_id not in seen:
            seen.add(model_id)
            choices.append(ModelChoice(model_id, reason_for(model_id)))
        if len(choices) >= limit:
            return tuple(choices)

    for model_id in available:
        if model_id in seen:
            continue
        if any(skip in model_id for skip in ("embed", "guard", "reward", "parse", "rerank", "vision")):
            continue
        if any(tag in model_id for tag in ("instruct", "nemotron", "deepseek", "qwen", "mistral", "gpt-oss")):
            seen.add(model_id)
            choices.append(ModelChoice(model_id, "discovered chat/instruct fallback"))
        if len(choices) >= limit:
            break
    return tuple(choices)


def reason_for(model_id: str) -> str:
    if "qwen3-coder" in model_id:
        return "code and symbolic reasoning specialist"
    if "nemotron" in model_id:
        return "NVIDIA reasoning-focused model"
    if "llama-4-maverick" in model_id:
        return "large MoE generalist"
    if "gpt-oss" in model_id:
        return "open-weight frontier baseline"
    if "deepseek-v4-flash" in model_id:
        return "fast reasoning baseline"
    if "mistral-large" in model_id:
        return "frontier instruction-following baseline"
    if "kimi" in model_id:
        return "long-context challenger"
    if "deepseek-v4-pro" in model_id:
        return "strong reasoning candidate, rate-limit sensitive"
    return "priority candidate"
