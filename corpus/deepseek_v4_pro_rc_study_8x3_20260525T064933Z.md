# LiveProof Model Study

Results file: `corpus/deepseek_v4_pro_rc_study_8x3_20260525T064933Z.results.jsonl`
Records: 24
Models: 1

## Model Leaderboard

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek-v4-pro` | 11 | 13 | 0 | 24 | 46% |

## Family Matrix

| Model | Family | Accepted | Total | Acceptance |
| --- | --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | `affine_mod` | 0 | 3 | 0% |
| `deepseek-v4-pro` | `boolean_count` | 2 | 3 | 67% |
| `deepseek-v4-pro` | `counterexample_search` | 1 | 3 | 33% |
| `deepseek-v4-pro` | `dfa_shortest` | 2 | 3 | 67% |
| `deepseek-v4-pro` | `graph_intervention` | 3 | 3 | 100% |
| `deepseek-v4-pro` | `grid_checksum` | 0 | 3 | 0% |
| `deepseek-v4-pro` | `program_trace` | 2 | 3 | 67% |
| `deepseek-v4-pro` | `string_rewrite` | 1 | 3 | 33% |

## Difficulty Matrix

| Model | Profile | Accepted | Total | Acceptance |
| --- | --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | `easy` | 6 | 8 | 75% |
| `deepseek-v4-pro` | `hard` | 1 | 8 | 12% |
| `deepseek-v4-pro` | `medium` | 4 | 8 | 50% |

## Difficulty x Family

| Model | Profile | Family | Accepted | Total | Acceptance |
| --- | --- | --- | ---: | ---: | ---: |
| `deepseek-v4-pro` | `easy` | `affine_mod` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `easy` | `boolean_count` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `easy` | `counterexample_search` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `easy` | `dfa_shortest` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `easy` | `graph_intervention` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `easy` | `grid_checksum` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `easy` | `program_trace` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `easy` | `string_rewrite` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `hard` | `affine_mod` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `boolean_count` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `counterexample_search` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `dfa_shortest` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `graph_intervention` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `hard` | `grid_checksum` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `program_trace` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `hard` | `string_rewrite` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `medium` | `affine_mod` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `medium` | `boolean_count` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `medium` | `counterexample_search` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `medium` | `dfa_shortest` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `medium` | `graph_intervention` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `medium` | `grid_checksum` | 0 | 1 | 0% |
| `deepseek-v4-pro` | `medium` | `program_trace` | 1 | 1 | 100% |
| `deepseek-v4-pro` | `medium` | `string_rewrite` | 0 | 1 | 0% |

## Failures

### deepseek-v4-pro / lp-affine_mod-0000-453314a6c338

- Family: `affine_mod`
- Profile: `easy`
- Task hash: `9df0826a5d0b0c660fb34137286a941f80e496e892308736473c013fe44fe4f4`
- Status: `rejected`
- Verifier: expected '(18, 6)', got ''
- Error: none

Prompt:

```text
Work modulo 19. Let x_0 = (15, 16). For t >= 0, x_(t+1) = A x_t + b, where A = [[2, 17], [9, 6]] and b = (14, 10). What is x_7? Return only the ordered pair as two integers, like (a, b).
```

Answer:

```text

```

### deepseek-v4-pro / lp-grid_checksum-0007-375ee3c72ebc

- Family: `grid_checksum`
- Profile: `easy`
- Task hash: `e1666e5a072b61394b251bd1dbb04274870528643b9d0694b7068e78cf8d19cb`
- Status: `rejected`
- Verifier: expected '710', got '163'
- Error: none

Prompt:

```text
On this 3x3 grid, rows are: 4 3 9; 4 0 1; 6 4 0. Start at row 2, column 2. Follow moves UDUUUDL with wraparound at edges. Checksum starts at 0; after visiting each new cell, checksum = (checksum*31 + cell_value) mod 997. Include the starting cell before moves. Return only the final checksum integer.
```

Answer:

```text
<answer>163</answer>
```

### deepseek-v4-pro / lp-affine_mod-0000-7f5a6773efed

- Family: `affine_mod`
- Profile: `medium`
- Task hash: `03a20387e1bfe4c6d65b550de43dae880875e3d3ade7e8847617854d7de3336d`
- Status: `rejected`
- Verifier: expected '(37, 54)', got ''
- Error: none

Prompt:

```text
Work modulo 101. Let x_0 = (64, 33). For t >= 0, x_(t+1) = A x_t + b, where A = [[64, 3], [45, 7]] and b = (67, 28). What is x_34? Return only the ordered pair as two integers, like (a, b).
```

Answer:

```text

```

### deepseek-v4-pro / lp-counterexample_search-0005-5167fb7f5d29

- Family: `counterexample_search`
- Profile: `medium`
- Task hash: `48af7ff69250d78af0fbf847c4db59ba760c8238cc765f135165759064d9cc3e`
- Status: `rejected`
- Verifier: expected '209', got ''
- Error: none

Prompt:

```text
Find the smallest integer x in [0, 303] satisfying all constraints: (13*x + 7) mod 18 = 6; (20*x + 6) mod 26 = 0; (16*x + 15) mod 20 = 19. Return only x.
```

Answer:

```text

```

### deepseek-v4-pro / lp-string_rewrite-0006-a0f009353cca

- Family: `string_rewrite`
- Profile: `medium`
- Task hash: `4b3d1ec1829a491d358e047a55b54688d98a8e8249bcefe7eedb887d89fa71f6`
- Status: `rejected`
- Verifier: expected '22222212022', got ''
- Error: none

Prompt:

```text
Start with circular string 01100211002. For each step, replace every position i simultaneously using the pair s[i]s[(i+1) mod n]. Rules: 00->1, 01->0, 02->2, 10->1, 11->2, 12->0, 20->2, 21->1, 22->2. After 8 steps, what is the string? Return only the final string.
```

Answer:

```text

```

### deepseek-v4-pro / lp-grid_checksum-0007-b415021fa3d1

- Family: `grid_checksum`
- Profile: `medium`
- Task hash: `f4abc4f72a0913c2dfa9b2abdfd8bcfdd283065db8b734d07427e0083747209c`
- Status: `rejected`
- Verifier: expected '575', got ''
- Error: none

Prompt:

```text
On this 6x6 grid, rows are: 4 0 4 3 4 4; 7 8 2 7 5 0; 8 5 6 0 8 6; 8 1 5 7 3 4; 5 4 5 4 7 4; 0 9 1 6 2 6. Start at row 0, column 3. Follow moves LUDLDRLULLUDLLLULDR with wraparound at edges. Checksum starts at 0; after visiting each new cell, checksum = (checksum*31 + cell_value) mod 3001. Include the starting cell before moves. Return only the final checksum integer.
```

Answer:

```text

```

### deepseek-v4-pro / lp-affine_mod-0000-91d088dd0315

- Family: `affine_mod`
- Profile: `hard`
- Task hash: `a959d93e3056d886ab5100bb296bc7d710ed58e728f4ac8f5cc8fb04ab60b821`
- Status: `rejected`
- Verifier: expected '(10, 72)', got ''
- Error: none

Prompt:

```text
Work modulo 139. Let x_0 = (3, 19). For t >= 0, x_(t+1) = A x_t + b, where A = [[49, 22], [127, 97]] and b = (12, 71). What is x_72? Return only the ordered pair as two integers, like (a, b).
```

Answer:

```text

```

### deepseek-v4-pro / lp-dfa_shortest-0001-9447df453ec1

- Family: `dfa_shortest`
- Profile: `hard`
- Task hash: `767abea02312ca540bada8406947a53752c2400fcc6c69d4f25ae0cb9723ad5e`
- Status: `rejected`
- Verifier: expected 'cda', got '<empty>'
- Error: none

Prompt:

```text
Given this deterministic finite automaton, find the lexicographically first shortest word over alphabet ['a', 'b', 'c', 'd'] that takes state 7 to state 0. Transitions: 0: a->5, b->9, c->9, d->4; 1: a->2, b->10, c->1, d->2; 2: a->4, b->2, c->0, d->9; 3: a->9, b->3, c->7, d->10; 4: a->8, b->6, c->8, d->10; 5: a->12, b->5, c->5, d->4; 6: a->1, b->9, c->2, d->2; 7: a->7, b->5, c->3, d->6; 8: a->6, b->4, c->11, d->5; 9: a->10, b->7, c->10, d->11; 10: a->0, b->3, c->3, d->1; 11: a->5, b->6, c->11, d->6; 12: a->6, b->6, c->6, d->7. Return only the word. If the empty word is correct, return <empty>.
```

Answer:

```text

```

### deepseek-v4-pro / lp-boolean_count-0003-472b61175b02

- Family: `boolean_count`
- Profile: `hard`
- Task hash: `ab27e91f835648aee431b736caea00bc025686ad628e9448bb53a3fef4d80171`
- Status: `rejected`
- Verifier: expected '23', got ''
- Error: none

Prompt:

```text
For Boolean variables ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'], how many assignments satisfy this CNF formula: (!x4 OR !x2) AND (!x8 OR x0 OR x4) AND (!x1 OR x0 OR x4) AND (!x0 OR !x1) AND (!x2 OR x7) AND (x3 OR !x1 OR x4) AND (!x4 OR !x5 OR x3) AND (x2 OR !x1 OR x3) AND (!x7 OR !x8 OR !x2) AND (x6 OR x5) AND (!x6 OR x8) AND (x7 OR !x2) AND (!x4 OR !x7) AND (!x6 OR x7) AND (!x8 OR !x1) AND (!x6 OR !x7 OR !x5) AND (x7 OR !x6)? Return only the integer count.
```

Answer:

```text

```

### deepseek-v4-pro / lp-program_trace-0004-12ed26b9677b

- Family: `program_trace`
- Profile: `hard`
- Task hash: `037389f3752845017b22dac7485e1a6e886229196219f66ce5d72db89f7151e2`
- Status: `rejected`
- Verifier: expected '(27, 27, 68)', got ''
- Error: none

Prompt:

```text
Registers r0,r1,r2 start as (63, 66, 2). Arithmetic is modulo 103. Execute these instructions in order: r2 = r2 + r1 + 86; r0 = r0 * (r1 + 1) + 89; r2 = r2 + 2*r0 + 63; r1 = r1 + 2*r0 + 43; r1 = r1 + 2*r1 + 10; r1 = r1 XOR r1 XOR 71; r0 = r0 + r0 + 73; r2 = r2 XOR r0 XOR 70; r0 = r0 + 2*r2 + 7; r0 = r0 * (r2 + 1) + 32; r1 = r1 + 2*r1 + 50; r0 = r0 XOR r0 XOR 74; r0 = r0 XOR r1 XOR 42; r0 = r0 + 2*r2 + 18; r1 = r1 + r1 + 87; r2 = r2 + r0 + 87; r0 = r0 + 2*r0 + 20; r1 = r1 XOR r1 XOR 27; r0 = r0 + 2*r1 + 32; r0 = r0 * (r1 + 1) + 71. Return only the final register tuple as (r0, r1, r2).
```

Answer:

```text

```

### deepseek-v4-pro / lp-counterexample_search-0005-75cd1ba937f1

- Family: `counterexample_search`
- Profile: `hard`
- Task hash: `28839304cf29962859e57ba60db652d950dfc5cda14d654360e27303157f4d88`
- Status: `rejected`
- Verifier: expected '757', got ''
- Error: none

Prompt:

```text
Find the smallest integer x in [0, 839] satisfying all constraints: (5*x + 12) mod 30 = 17; (4*x + 0) mod 17 = 2; (9*x + 22) mod 38 = 33; (8*x + 9) mod 31 = 20. Return only x.
```

Answer:

```text

```

### deepseek-v4-pro / lp-string_rewrite-0006-6e75def01069

- Family: `string_rewrite`
- Profile: `hard`
- Task hash: `b5f11555ae75d383463ac139706d6c84e1d4e96a1cd104d274420691cf88cf10`
- Status: `rejected`
- Verifier: expected '133331313002', got ''
- Error: none

Prompt:

```text
Start with circular string 130221321211. For each step, replace every position i simultaneously using the pair s[i]s[(i+1) mod n]. Rules: 00->3, 01->2, 02->1, 03->0, 10->2, 11->0, 12->0, 13->3, 20->3, 21->3, 22->1, 23->2, 30->1, 31->3, 32->1, 33->1. After 16 steps, what is the string? Return only the final string.
```

Answer:

```text

```

### deepseek-v4-pro / lp-grid_checksum-0007-c6fbff155522

- Family: `grid_checksum`
- Profile: `hard`
- Task hash: `89bbfad0a03c9eea5c6d843d5cd7f6d7a0b3785bc05e4c37d77fdb17f1f08254`
- Status: `rejected`
- Verifier: expected '6392', got ''
- Error: none

Prompt:

```text
On this 8x8 grid, rows are: 9 7 7 9 4 7 6 0; 9 3 6 0 8 9 4 7; 6 7 2 1 9 0 5 6; 2 8 6 5 5 4 4 9; 8 7 2 7 1 7 1 7; 2 2 1 3 3 1 7 4; 2 9 3 6 7 6 0 3; 8 3 0 0 4 6 1 4. Start at row 3, column 2. Follow moves URLLLULLDRRLULUDDDUDDLDRRUDUUUURRULDRRUDULUDLLRUDRUURDUUUDRLDLULD with wraparound at edges. Checksum starts at 0; after visiting each new cell, checksum = (checksum*31 + cell_value) mod 10007. Include the starting cell before moves. Return only the final checksum integer.
```

Answer:

```text

```

