from __future__ import annotations

import itertools
import re
from collections import deque

from .generators import (
    _apply_rewrite,
    _grid_checksum_value,
    _literal_value,
    _run_program,
    _solve_counterexample,
)
from .schema import Task


def solve(task: Task) -> str:
    verifier_type = task.verifier["type"]
    if verifier_type == "affine_mod":
        return _solve_affine(task.verifier)
    if verifier_type == "dfa_shortest":
        return _solve_dfa(task.verifier)
    if verifier_type == "graph_intervention":
        return _solve_graph(task.verifier)
    if verifier_type == "boolean_count":
        return _solve_boolean(task.verifier)
    if verifier_type == "program_trace":
        return _solve_program_trace(task.verifier)
    if verifier_type == "counterexample_search":
        return _solve_counterexample_search(task.verifier)
    if verifier_type == "string_rewrite":
        return _solve_string_rewrite(task.verifier)
    if verifier_type == "grid_checksum":
        return _solve_grid_checksum(task.verifier)
    raise ValueError(f"Unknown verifier type: {verifier_type}")


def verify(task: Task, answer: str) -> tuple[bool, str]:
    expected = solve(task)
    submitted = _normalize_answer(task.verifier, answer)
    ok = submitted == expected
    if ok:
        return True, "accepted"
    return False, f"expected {expected!r}, got {submitted!r}"


def _normalize_answer(verifier: dict, answer: str) -> str:
    verifier_type = verifier["type"]
    text = _extract_answer(answer.strip())
    if verifier_type == "affine_mod":
        numbers = re.findall(r"-?\d+", text)
        if len(numbers) >= 2:
            return f"({int(numbers[0])}, {int(numbers[1])})"
    if verifier_type == "dfa_shortest":
        if text in {"", "<empty>", "epsilon", "ε"}:
            return "<empty>"
        alphabet = "".join(re.escape(symbol) for symbol in verifier.get("alphabet", ["a", "b", "c"]))
        return re.sub(rf"[^{alphabet}]", "", text.lower())
    if verifier_type == "graph_intervention":
        lowered = text.lower()
        if lowered.startswith("y"):
            return "yes"
        if lowered.startswith("n"):
            return "no"
    if verifier_type == "boolean_count":
        match = re.search(r"-?\d+", text)
        if match:
            return str(int(match.group(0)))
    if verifier_type == "program_trace":
        numbers = re.findall(r"-?\d+", text)
        if len(numbers) >= 3:
            return f"({int(numbers[0])}, {int(numbers[1])}, {int(numbers[2])})"
    if verifier_type == "counterexample_search":
        match = re.search(r"-?\d+", text)
        if match:
            return str(int(match.group(0)))
    if verifier_type == "string_rewrite":
        alphabet = "".join(re.escape(symbol) for symbol in verifier.get("alphabet", ["0", "1", "2"]))
        return "".join(re.findall(rf"[{alphabet}]", text))
    if verifier_type == "grid_checksum":
        match = re.search(r"-?\d+", text)
        if match:
            return str(int(match.group(0)))
    return text


def _extract_answer(answer: str) -> str:
    match = re.search(r"<answer>\s*(.*?)\s*</answer>", answer, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return answer.strip()


def _solve_affine(verifier: dict) -> str:
    prime = verifier["prime"]
    matrix = verifier["matrix"]
    bias = verifier["bias"]
    state = verifier["state"][:]
    for _ in range(verifier["steps"]):
        state = [
            (matrix[0][0] * state[0] + matrix[0][1] * state[1] + bias[0]) % prime,
            (matrix[1][0] * state[0] + matrix[1][1] * state[1] + bias[1]) % prime,
        ]
    return f"({state[0]}, {state[1]})"


def _solve_dfa(verifier: dict) -> str:
    transitions = verifier["transitions"]
    alphabet = verifier["alphabet"]
    start = verifier["start"]
    target = verifier["target"]
    queue = deque([(start, "")])
    seen = {start}
    while queue:
        state, word = queue.popleft()
        if state == target:
            return word or "<empty>"
        for symbol in alphabet:
            nxt = transitions[str(state)][symbol]
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, word + symbol))
    raise ValueError("DFA target is unreachable")


def _solve_graph(verifier: dict) -> str:
    nodes = verifier["nodes"]
    edges = {tuple(edge) for edge in verifier["edges"]}
    edges.discard(tuple(verifier["remove"]))
    source = verifier["source"]
    target = verifier["target"]
    graph = {node: [] for node in range(nodes)}
    for src, dst in edges:
        graph[src].append(dst)
    queue = deque([source])
    seen = {source}
    while queue:
        node = queue.popleft()
        if node == target:
            return "yes"
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return "no"


def _solve_boolean(verifier: dict) -> str:
    variables = verifier["variables"]
    clauses = verifier["clauses"]
    count = 0
    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(any(_literal_value(lit, assignment) for lit in clause) for clause in clauses):
            count += 1
    return str(count)


def _solve_program_trace(verifier: dict) -> str:
    result = _run_program(verifier["registers"], verifier["instructions"], verifier["modulus"])
    return f"({result[0]}, {result[1]}, {result[2]})"


def _solve_counterexample_search(verifier: dict) -> str:
    return str(_solve_counterexample(verifier["upper"], verifier["constraints"]))


def _solve_string_rewrite(verifier: dict) -> str:
    return _apply_rewrite(verifier["initial"], verifier["rules"], verifier["steps"])


def _solve_grid_checksum(verifier: dict) -> str:
    return str(_grid_checksum_value(verifier["grid"], verifier["start"], verifier["moves"], verifier["modulus"]))
