from __future__ import annotations

import itertools
import random
from collections import deque

from .schema import Task, stable_hash


FAMILIES = (
    "affine_mod",
    "dfa_shortest",
    "graph_intervention",
    "boolean_count",
    "program_trace",
    "counterexample_search",
    "string_rewrite",
    "grid_checksum",
)


def generate_tasks(seed: str, count: int, profile: str = "medium") -> list[Task]:
    if profile not in {"easy", "medium", "hard", "extreme"}:
        raise ValueError(f"Unknown profile: {profile}")
    tasks: list[Task] = []
    for index in range(count):
        family = FAMILIES[index % len(FAMILIES)]
        rng = random.Random(f"{seed}:{profile}:{index}:{family}")
        if family == "affine_mod":
            task = _affine_mod(seed, index, rng, profile)
        elif family == "dfa_shortest":
            task = _dfa_shortest(seed, index, rng, profile)
        elif family == "graph_intervention":
            task = _graph_intervention(seed, index, rng, profile)
        elif family == "boolean_count":
            task = _boolean_count(seed, index, rng, profile)
        elif family == "program_trace":
            task = _program_trace(seed, index, rng, profile)
        elif family == "counterexample_search":
            task = _counterexample_search(seed, index, rng, profile)
        elif family == "string_rewrite":
            task = _string_rewrite(seed, index, rng, profile)
        elif family == "grid_checksum":
            task = _grid_checksum(seed, index, rng, profile)
        else:
            raise ValueError(f"Unknown family: {family}")
        tasks.append(task)
    return tasks


def _task_id(seed: str, index: int, family: str, payload: dict) -> str:
    digest = stable_hash({"seed": seed, "index": index, "family": family, "payload": payload})[:12]
    return f"lp-{family}-{index:04d}-{digest}"


def _affine_mod(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        primes = [17, 19, 23, 29, 31]
        steps_range = (4, 8)
    elif profile == "extreme":
        primes = [251, 257, 263, 269, 271, 277]
        steps_range = (180, 420)
    elif profile == "hard":
        primes = [127, 131, 137, 139, 149, 151]
        steps_range = (55, 95)
    else:
        primes = [97, 101, 103, 107, 109, 113, 127]
        steps_range = (18, 45)
    prime = rng.choice(primes)
    matrix = [[rng.randrange(prime) for _ in range(2)] for _ in range(2)]
    bias = [rng.randrange(prime) for _ in range(2)]
    state = [rng.randrange(prime) for _ in range(2)]
    steps = rng.randint(*steps_range)

    result = state[:]
    for _ in range(steps):
        result = [
            (matrix[0][0] * result[0] + matrix[0][1] * result[1] + bias[0]) % prime,
            (matrix[1][0] * result[0] + matrix[1][1] * result[1] + bias[1]) % prime,
        ]

    verifier = {
        "type": "affine_mod",
        "profile": profile,
        "prime": prime,
        "matrix": matrix,
        "bias": bias,
        "state": state,
        "steps": steps,
    }
    prompt = (
        f"Work modulo {prime}. Let x_0 = ({state[0]}, {state[1]}). "
        f"For t >= 0, x_(t+1) = A x_t + b, where "
        f"A = [[{matrix[0][0]}, {matrix[0][1]}], [{matrix[1][0]}, {matrix[1][1]}]] "
        f"and b = ({bias[0]}, {bias[1]}). What is x_{steps}? "
        "Return only the ordered pair as two integers, like (a, b)."
    )
    return Task(_task_id(seed, index, "affine_mod", verifier), "affine_mod", seed, prompt, verifier, f"({result[0]}, {result[1]})")


def _dfa_shortest(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        states = rng.randint(4, 5)
        alphabet = ["a", "b"]
    elif profile == "extreme":
        states = rng.randint(18, 26)
        alphabet = ["a", "b", "c", "d", "e"]
    elif profile == "hard":
        states = rng.randint(10, 14)
        alphabet = ["a", "b", "c", "d"]
    else:
        states = rng.randint(6, 9)
        alphabet = ["a", "b", "c"]
    transitions = {
        str(state): {symbol: rng.randrange(states) for symbol in alphabet}
        for state in range(states)
    }
    start = rng.randrange(states)
    target = rng.randrange(states)
    while target == start:
        target = rng.randrange(states)

    word = _shortest_word(transitions, start, target, alphabet)
    if word is None:
        transitions[str(start)]["a"] = target
        word = "a"

    verifier = {
        "type": "dfa_shortest",
        "profile": profile,
        "states": states,
        "alphabet": alphabet,
        "transitions": transitions,
        "start": start,
        "target": target,
    }
    table = "; ".join(
        f"{state}: " + ", ".join(f"{sym}->{dst}" for sym, dst in transitions[str(state)].items())
        for state in range(states)
    )
    prompt = (
        "Given this deterministic finite automaton, find the lexicographically first shortest word "
        f"over alphabet {alphabet} that takes state {start} to state {target}. "
        f"Transitions: {table}. Return only the word. If the empty word is correct, return <empty>."
    )
    return Task(_task_id(seed, index, "dfa_shortest", verifier), "dfa_shortest", seed, prompt, verifier, word or "<empty>")


def _shortest_word(transitions: dict[str, dict[str, int]], start: int, target: int, alphabet: list[str]) -> str | None:
    queue = deque([(start, "")])
    seen = {start}
    while queue:
        state, word = queue.popleft()
        if state == target:
            return word
        for symbol in alphabet:
            nxt = transitions[str(state)][symbol]
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, word + symbol))
    return None


def _graph_intervention(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        nodes = rng.randint(5, 7)
        edge_probability = 0.34
    elif profile == "extreme":
        nodes = rng.randint(28, 42)
        edge_probability = 0.13
    elif profile == "hard":
        nodes = rng.randint(14, 20)
        edge_probability = 0.2
    else:
        nodes = rng.randint(8, 12)
        edge_probability = 0.28
    edges: set[tuple[int, int]] = set()
    for src in range(nodes):
        for dst in range(src + 1, nodes):
            if rng.random() < edge_probability:
                edges.add((src, dst))
    source, target = 0, nodes - 1
    if not _reachable(nodes, edges, source, target):
        chain = [(i, i + 1) for i in range(nodes - 1)]
        edges.update(chain)
    removed = rng.choice(sorted(edges))
    answer = "yes" if _reachable(nodes, edges - {removed}, source, target) else "no"

    verifier = {
        "type": "graph_intervention",
        "profile": profile,
        "nodes": nodes,
        "edges": sorted([list(edge) for edge in edges]),
        "remove": list(removed),
        "source": source,
        "target": target,
    }
    prompt = (
        f"A directed acyclic graph has nodes 0 through {nodes - 1}. "
        f"Edges are {sorted(edges)}. Delete edge {removed}. "
        f"After deletion, is there still a directed path from {source} to {target}? "
        "Return only yes or no."
    )
    return Task(_task_id(seed, index, "graph_intervention", verifier), "graph_intervention", seed, prompt, verifier, answer)


def _reachable(nodes: int, edges: set[tuple[int, int]], source: int, target: int) -> bool:
    graph = {node: [] for node in range(nodes)}
    for src, dst in edges:
        graph[src].append(dst)
    queue = deque([source])
    seen = {source}
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def _boolean_count(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        variable_count = rng.randint(3, 4)
        clause_count = rng.randint(3, 5)
    elif profile == "extreme":
        variable_count = rng.randint(12, 14)
        clause_count = rng.randint(22, 34)
    elif profile == "hard":
        variable_count = rng.randint(8, 10)
        clause_count = rng.randint(12, 18)
    else:
        variable_count = rng.randint(5, 7)
        clause_count = rng.randint(5, 9)
    variables = [f"x{i}" for i in range(variable_count)]
    clauses: list[list[str]] = []
    for _ in range(clause_count):
        width = rng.randint(2, 3)
        chosen = rng.sample(variables, width)
        clause = [var if rng.random() < 0.5 else f"!{var}" for var in chosen]
        clauses.append(clause)

    count = 0
    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(any(_literal_value(lit, assignment) for lit in clause) for clause in clauses):
            count += 1

    verifier = {"type": "boolean_count", "profile": profile, "variables": variables, "clauses": clauses}
    formula = " AND ".join("(" + " OR ".join(clause) + ")" for clause in clauses)
    prompt = (
        f"For Boolean variables {variables}, how many assignments satisfy this CNF formula: "
        f"{formula}? Return only the integer count."
    )
    return Task(_task_id(seed, index, "boolean_count", verifier), "boolean_count", seed, prompt, verifier, str(count))


def _literal_value(literal: str, assignment: dict[str, bool]) -> bool:
    if literal.startswith("!"):
        return not assignment[literal[1:]]
    return assignment[literal]


def _program_trace(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        modulus = rng.choice([17, 19, 23])
        instruction_count = rng.randint(5, 7)
    elif profile == "extreme":
        modulus = rng.choice([251, 257, 263, 269])
        instruction_count = rng.randint(80, 140)
    elif profile == "hard":
        modulus = rng.choice([101, 103, 107, 109])
        instruction_count = rng.randint(18, 26)
    else:
        modulus = rng.choice([41, 43, 47, 53])
        instruction_count = rng.randint(10, 15)
    registers = [rng.randrange(modulus) for _ in range(3)]
    instructions = []
    for _ in range(instruction_count):
        op = rng.choice(["add", "mul", "xor", "mix"])
        dst = rng.randrange(3)
        src = rng.randrange(3)
        value = rng.randrange(modulus)
        instructions.append({"op": op, "dst": dst, "src": src, "value": value})
    result = _run_program(registers, instructions, modulus)
    verifier = {
        "type": "program_trace",
        "profile": profile,
        "modulus": modulus,
        "registers": registers,
        "instructions": instructions,
    }
    rendered = "; ".join(_render_instruction(item) for item in instructions)
    prompt = (
        f"Registers r0,r1,r2 start as {tuple(registers)}. Arithmetic is modulo {modulus}. "
        "Execute these instructions in order: "
        f"{rendered}. Return only the final register tuple as (r0, r1, r2)."
    )
    return Task(_task_id(seed, index, "program_trace", verifier), "program_trace", seed, prompt, verifier, f"({result[0]}, {result[1]}, {result[2]})")


def _run_program(registers: list[int], instructions: list[dict], modulus: int) -> list[int]:
    state = registers[:]
    for item in instructions:
        dst = item["dst"]
        src = item["src"]
        value = item["value"]
        if item["op"] == "add":
            state[dst] = (state[dst] + state[src] + value) % modulus
        elif item["op"] == "mul":
            state[dst] = (state[dst] * (state[src] + 1) + value) % modulus
        elif item["op"] == "xor":
            state[dst] = (state[dst] ^ state[src] ^ value) % modulus
        elif item["op"] == "mix":
            state[dst] = (state[dst] + 2 * state[src] + value) % modulus
        else:
            raise ValueError(f"Unknown op: {item['op']}")
    return state


def _render_instruction(item: dict) -> str:
    dst = f"r{item['dst']}"
    src = f"r{item['src']}"
    value = item["value"]
    if item["op"] == "add":
        return f"{dst} = {dst} + {src} + {value}"
    if item["op"] == "mul":
        return f"{dst} = {dst} * ({src} + 1) + {value}"
    if item["op"] == "xor":
        return f"{dst} = {dst} XOR {src} XOR {value}"
    if item["op"] == "mix":
        return f"{dst} = {dst} + 2*{src} + {value}"
    raise ValueError(f"Unknown op: {item['op']}")


def _counterexample_search(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        upper = rng.randint(25, 60)
        constraint_count = 2
        moduli = [rng.randint(5, 13) for _ in range(constraint_count)]
    elif profile == "extreme":
        upper = rng.randint(5000, 15000)
        constraint_count = 5
        moduli = [rng.randint(31, 97) for _ in range(constraint_count)]
    elif profile == "hard":
        upper = rng.randint(500, 1200)
        constraint_count = 4
        moduli = [rng.randint(17, 41) for _ in range(constraint_count)]
    else:
        upper = rng.randint(120, 350)
        constraint_count = 3
        moduli = [rng.randint(11, 29) for _ in range(constraint_count)]
    witness = rng.randint(0, upper)
    constraints = []
    for modulus in moduli:
        a = rng.randint(1, modulus - 1)
        b = rng.randint(0, modulus - 1)
        residue = (a * witness + b) % modulus
        constraints.append({"a": a, "b": b, "modulus": modulus, "residue": residue})
    answer = _solve_counterexample(upper, constraints)
    verifier = {
        "type": "counterexample_search",
        "profile": profile,
        "upper": upper,
        "constraints": constraints,
    }
    rendered = "; ".join(
        f"({item['a']}*x + {item['b']}) mod {item['modulus']} = {item['residue']}"
        for item in constraints
    )
    prompt = (
        f"Find the smallest integer x in [0, {upper}] satisfying all constraints: "
        f"{rendered}. Return only x."
    )
    return Task(_task_id(seed, index, "counterexample_search", verifier), "counterexample_search", seed, prompt, verifier, str(answer))


def _solve_counterexample(upper: int, constraints: list[dict]) -> int:
    for x in range(upper + 1):
        if all((item["a"] * x + item["b"]) % item["modulus"] == item["residue"] for item in constraints):
            return x
    raise ValueError("Generated constraints have no solution")


def _string_rewrite(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    alphabet = ["0", "1", "2"] if profile in {"easy", "medium"} else ["0", "1", "2", "3"]
    if profile == "easy":
        length = rng.randint(5, 7)
        steps = rng.randint(3, 5)
    elif profile == "extreme":
        length = rng.randint(28, 44)
        steps = rng.randint(80, 160)
    elif profile == "hard":
        length = rng.randint(12, 18)
        steps = rng.randint(12, 20)
    else:
        length = rng.randint(8, 12)
        steps = rng.randint(6, 10)
    initial = "".join(rng.choice(alphabet) for _ in range(length))
    rules = {
        left + right: rng.choice(alphabet)
        for left in alphabet
        for right in alphabet
    }
    answer = _apply_rewrite(initial, rules, steps)
    verifier = {
        "type": "string_rewrite",
        "profile": profile,
        "alphabet": alphabet,
        "initial": initial,
        "rules": rules,
        "steps": steps,
    }
    rendered = ", ".join(f"{pair}->{value}" for pair, value in sorted(rules.items()))
    prompt = (
        f"Start with circular string {initial}. For each step, replace every position i "
        "simultaneously using the pair s[i]s[(i+1) mod n]. "
        f"Rules: {rendered}. After {steps} steps, what is the string? Return only the final string."
    )
    return Task(_task_id(seed, index, "string_rewrite", verifier), "string_rewrite", seed, prompt, verifier, answer)


def _apply_rewrite(initial: str, rules: dict[str, str], steps: int) -> str:
    state = initial
    for _ in range(steps):
        state = "".join(rules[state[i] + state[(i + 1) % len(state)]] for i in range(len(state)))
    return state


def _grid_checksum(seed: str, index: int, rng: random.Random, profile: str) -> Task:
    if profile == "easy":
        size = rng.randint(3, 4)
        move_count = rng.randint(6, 10)
        modulus = 997
    elif profile == "extreme":
        size = rng.randint(12, 16)
        move_count = rng.randint(180, 320)
        modulus = 1000003
    elif profile == "hard":
        size = rng.randint(7, 9)
        move_count = rng.randint(40, 70)
        modulus = 10007
    else:
        size = rng.randint(5, 6)
        move_count = rng.randint(18, 32)
        modulus = 3001
    grid = [[rng.randint(0, 9) for _ in range(size)] for _ in range(size)]
    start = [rng.randrange(size), rng.randrange(size)]
    moves = "".join(rng.choice("UDLR") for _ in range(move_count))
    checksum = _grid_checksum_value(grid, start, moves, modulus)
    verifier = {
        "type": "grid_checksum",
        "profile": profile,
        "size": size,
        "grid": grid,
        "start": start,
        "moves": moves,
        "modulus": modulus,
    }
    rows = "; ".join(" ".join(str(cell) for cell in row) for row in grid)
    prompt = (
        f"On this {size}x{size} grid, rows are: {rows}. Start at row {start[0]}, column {start[1]}. "
        f"Follow moves {moves} with wraparound at edges. Checksum starts at 0; after visiting each new cell, "
        f"checksum = (checksum*31 + cell_value) mod {modulus}. Include the starting cell before moves. "
        "Return only the final checksum integer."
    )
    return Task(_task_id(seed, index, "grid_checksum", verifier), "grid_checksum", seed, prompt, verifier, str(checksum))


def _grid_checksum_value(grid: list[list[int]], start: list[int], moves: str, modulus: int) -> int:
    size = len(grid)
    row, col = start
    checksum = grid[row][col] % modulus
    for move in moves:
        if move == "U":
            row = (row - 1) % size
        elif move == "D":
            row = (row + 1) % size
        elif move == "L":
            col = (col - 1) % size
        elif move == "R":
            col = (col + 1) % size
        else:
            raise ValueError(f"Unknown move: {move}")
        checksum = (checksum * 31 + grid[row][col]) % modulus
    return checksum
