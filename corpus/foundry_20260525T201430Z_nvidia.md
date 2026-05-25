# LiveProof Model Study

Results file: `/root/liveproof-agent/corpus/foundry_20260525T201430Z_nvidia.results.jsonl`
Records: 2
Models: 1

## Model Leaderboard

| Model | Accepted | Rejected | Errors | Total | Acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| `nvidia/nemotron-3-super-120b-a12b` | 0 | 2 | 0 | 2 | 0% |

## Family Matrix

| Model | Family | Accepted | Total | Acceptance |
| --- | --- | ---: | ---: | ---: |
| `nvidia/nemotron-3-super-120b-a12b` | `affine_mod` | 0 | 1 | 0% |
| `nvidia/nemotron-3-super-120b-a12b` | `dfa_shortest` | 0 | 1 | 0% |

## Difficulty Matrix

| Model | Profile | Accepted | Total | Acceptance |
| --- | --- | ---: | ---: | ---: |
| `nvidia/nemotron-3-super-120b-a12b` | `extreme` | 0 | 2 | 0% |

## Difficulty x Family

| Model | Profile | Family | Accepted | Total | Acceptance |
| --- | --- | --- | ---: | ---: | ---: |
| `nvidia/nemotron-3-super-120b-a12b` | `extreme` | `affine_mod` | 0 | 1 | 0% |
| `nvidia/nemotron-3-super-120b-a12b` | `extreme` | `dfa_shortest` | 0 | 1 | 0% |

## Failures

### nvidia/nemotron-3-super-120b-a12b / lp-affine_mod-0000-48531ea68818

- Family: `affine_mod`
- Profile: `extreme`
- Task hash: `b5bd831100360922db33db2b90939ef04b84c45276c3b56ec30ce45a34c15221`
- Status: `rejected`
- Verifier: expected '(217, 6)', got '(391, 1)'
- Error: none

Prompt:

```text
Work modulo 257. Let x_0 = (252, 112). For t >= 0, x_(t+1) = A x_t + b, where A = [[142, 55], [183, 198]] and b = (94, 254). What is x_391? Return only the ordered pair as two integers, like (a, b).
```

Answer:

```text
We need to compute x_t after 391 steps of linear recurrence: x_{t+1} = A x_t + b mod 257. Starting x0 = (252,112). Need x_391.

We can treat as affine transformation: x_t = A^t x_0 + (A^{t-1} + A^{t-2} + ... + I) b (if t>0). Actually formula: x_t = A^t x_0 + (sum_{i=0}^{t-1} A^i) b.

We need compute modulo prime 257. A is 2x2 matrix. Compute A^t and sum of powers.

We can compute using exponentiation by squaring, also compute geometric series of matrices.

Alternatively, we can augment to homogeneous coordinates: define y_t = [x_t; 1] (3-dim). Then y_{t+1} = M y_t where M = [[A, b]; [0,0,1]]? Actually for affine: [x_{t+1}; 1] = [[A, b]; [0 0 1]] * [x_t; 1]. So M is 3x3 matrix. Then y_t = M^t y_0. Compute M^391 * y0, then extract x.

We can compute M^391 mod 257 using fast exponentiation. Since dimension 3, manageable.

Let's do manually? Might be tedious but we can try to compute using some reasoning: maybe A has some order dividing something (since modulo prime). Could compute eigenvalues? But easier to compute using repeated squaring with some help.

We can attempt to compute using Python mentally? Might be long. Let's try to find pattern: maybe A is something like [[142,55],[183,198]] mod 257. Compute its trace and determinant.

Trace = 142+198 = 340 mod 257 = 340-257=83.

Determinant = 142*198 - 55*183 mod 257.

Compute 142*198: 142*200=28400 minus 142*2=284 => 28400-284=28116. Mod 257: compute 257*109 = 257*100=25700, +257*9=2313 => 28013. Subtract: 28116-28013=103. So 142*198 ≡ 103 mod 257.

Now 55*183: 55*180=9900, +55*3=165 => 10065. Mod 257: 257*39 = 257*40 -257 = 10280-257=10023. Subtract: 10065-10023=42. So 55*183 ≡ 42.

Thus determinant = 103 - 42 = 61 mod 257.

So det(A)=61.

We might compute order of A in GL(2,257). The group order is (257^2-1)*(257^2-257) = (66049-1)*(66049-257) = 66048*65792. That's huge. But maybe A has small order? Not likely.

We could compute M^t using exponentiation by squaring manually? Might be heavy but doable with careful steps.

Alternative: compute using formula for affine recurrence: x_t = A^t x0 + (A^t - I)*(A - I)^{-1} b, provided (A - I) invertible. Since we are in a field, if A-I invertible then sum_{i=0}^{t-1} A^i = (A^t - I)*(A - I)^{-1}. So we need to compute A^t and (A-I)^{-1}. That might be easier: compute A^t via fast exponentiation (2x2). Then compute (A-I)^{-1} (2x2 inverse). Then compute sum = (A^t - I)*(A-I)^{-1}. Then multiply by b and add A^t x0.

Thus we need to compute A^391 mod 257.

Let's attempt to compute A^391 via binary exponentiation. 391 in binary: 391 = 256 + 128 + 4 + 2 + 1? Let's check: 256+128=384, remainder 7 => 4+2+1=7. So yes: bits: 256 (2^8), 128 (2^7), 4 (2^2), 2 (2^1), 1 (2^0). So we need A^1, A^2, A^4, A^8, A^16, A^32, A^64, A^128, A^256. Multiply those corresponding.

We can compute powers by squaring.

Let's define matrix multiplication mod 257.

Let A = [[a,b],[c,d]] where a=142, b=55, c=183, d=198.

We'll compute A^2, A^4, A^8, etc.

We need to be careful with arithmetic mod 257.

I'll create a table.

First, compute A^1 = A.

Now compute A^2 = A * A.

Compute:

Top-left: a*a + b*c = 142*142 + 55*183.

Compute 142*142: 140*142=19880, plus 2*142=284 => 20164? Wait let's compute precisely: 142*142 = (100+40+2)*(100+40+2) = 10000 + 4000+200 + 4000+1600+80 +200+80+4 = 10000+8000+? Let's just do multiplication: 142*142 = 142*(100+40+2) = 14200 + 5680 + 284 = 20164. Yes.

Now 55*183 we already computed = 42? Wait earlier we computed 55*183 = 42 mod 257. But that was mod 257; we need actual product then mod. 55*183 = 10065. So compute 20164 + 10065 = 30229. Now mod 257: compute 257*117 = 257*100=25700, +257*17=4369 => 30069. Subtract: 30229-30069=160. So top-left = 160 mod 257.

Top-right: a*b + b*d = 142*55 + 55*198.

Compute 142*55 = 142*50 + 142*5 = 7100 + 710 = 7810.

55*198 = 55*200 - 55*2 = 11000 - 110 = 10890.

Sum = 7810+10890=18700. Mod 257: 257*72 = 257*70=17990, +257*2=514 => 18504. Subtract: 18700-18504=196. So top-right = 196.

Bottom-left: c*a + d*c = 183*142 + 198*183.

Compute 183*142 = 183*100 + 183*40 + 183*2 = 18300 + 7320 + 366 = 25986.

198*183 = (200-2)*183 = 36600 - 366 = 36234.

Sum =
```

### nvidia/nemotron-3-super-120b-a12b / lp-dfa_shortest-0001-2d07d91816bb

- Family: `dfa_shortest`
- Profile: `extreme`
- Task hash: `e650e69181debc0834789968b32e25ee844b3c9355097324eed305092277dacf`
- Status: `rejected`
- Verifier: expected 'cb', got 'eeeddecacaedeaabeabcdeaaeaeaeeaeadaaeaaeeedeacaedeaeebaeceecacaaedecaeecacadeabcdeeedcecacaaeeeedcebaaeacdaceadecacaadeacaeaeacdaceacabededaceecaaeedeceadecaaceedeeebeedecacaaaaeacebeeededeaabeedbeeeeeeebaabecadeeeeeacaeaebeaecacaaeeaeceabeeedaceecededeadeacdeeeeedeaabecadeeeeedceeaeaebeaeecacaaeaaeaeadadbeedaeeeacedeaaabecaaceeaeecacaaeaaeaceaeedbaebaeadeacaeecedeedeeeedceedcdeedeaedeadeacdeecdeedeaabecadeeeeeeacaebeaecacaaeaeaeabeeaeecacdeeeaeeaceedeedeeeedceedadeeadedeaabecadeacaaeaecacbeaeeeeebaeeeaabecaededeedaedceedaaeecacdeeaceeecdeceadaceeaeeadaceecdeaedeaabecadeeeeeeaeecedecaeeeaeeaedeecaaceaaeeacabebaedeeaedceedaaeeabeceeeedeeadaeaeeadceeaeaaaecabeaededceedecdeaeaeeaeeaaeaeaecdaececacaeeeaedeeeaaeaeebedceedaababeecacaaebecaeedeeadaeaaaecaabedceedeaedeeaedceedeceaadeeaeaeeeaeaebaadabbeecacaaeabbceadaceedceaeaaebeeaeaeaeadabaeaabadeaeaebeadaaaeabaecedacededeedeeacedbaaeaedeeacedbbaebeeeadaeaecdeedeaabecadeaebecaeedebeadaeedceaeaabeceabedeeeaaeedadedceaedabcecacaaedbcdeceaeeeecacaaeaeacaaceaeaebecaaceaaeaacaeeaeaaaeaaabecacaaeeadeaecaeecacaaeeaaeeaebecaaceaaeabaceeedeaabecadecedceaaeeacabebaadacebeeaaeeacabebbadaceeeeaeaaaeaebedceedeacabeaaaededeaeaebeeabedeaeceedeebeaeeaaaaebeaeeacedadaceaababeaeaeeebadeadaceaaaeceedbeeadaceabdeeecdedaceaeceeddeacdeeadeecdeecdadeecbeeacdebdeeeaaeeedecacdeaaaeaeeedbeeaabeeabeeadaabecaededeedecacdeeabaeeeeceaeedecacaaeeecadbaeeededeabcdeadeeeacaeecdeaeeedeccedeeedeeedeceadecaaceedeeeeaaeaeaeaeeaeacaeeeeceaaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaeabcdeaaeaeebaaecedaceadedeceaeaadacedeaaeeeaeeedeadecebeeaeedeededececaeccedbebeeceaeaabeaeeaecaedaddaceaaedeeeeedceaeaabcd'
- Error: none

Prompt:

```text
Given this deterministic finite automaton, find the lexicographically first shortest word over alphabet ['a', 'b', 'c', 'd', 'e'] that takes state 12 to state 6. Transitions: 0: a->15, b->15, c->6, d->9, e->18; 1: a->3, b->3, c->5, d->18, e->15; 2: a->15, b->8, c->10, d->20, e->0; 3: a->3, b->6, c->10, d->12, e->19; 4: a->1, b->10, c->14, d->18, e->16; 5: a->9, b->14, c->13, d->13, e->5; 6: a->18, b->17, c->11, d->16, e->17; 7: a->4, b->14, c->19, d->9, e->16; 8: a->12, b->18, c->7, d->0, e->5; 9: a->3, b->19, c->4, d->13, e->6; 10: a->16, b->6, c->7, d->4, e->0; 11: a->12, b->20, c->9, d->5, e->13; 12: a->1, b->2, c->10, d->19, e->9; 13: a->16, b->13, c->0, d->17, e->4; 14: a->11, b->18, c->1, d->8, e->10; 15: a->14, b->1, c->20, d->20, e->20; 16: a->12, b->3, c->2, d->20, e->13; 17: a->6, b->17, c->3, d->16, e->1; 18: a->5, b->11, c->9, d->12, e->6; 19: a->18, b->13, c->7, d->3, e->10; 20: a->15, b->6, c->14, d->3, e->7. Return only the word. If the empty word is correct, return <empty>.
```

Answer:

```text
We need to find lexicographically first shortest word over alphabet ['a','b','c','d','e'] that takes state 12 to state 6.

We have a DFA with states 0-20. Starting state: 12. Need to reach state 6. Find shortest path (fewest symbols) from 12 to 6. Among those, choose lexicographically smallest word (i.e., compare strings lexicographically with order a<b<c<d<e). If multiple shortest words, pick lexicographically smallest.

We need to compute BFS from start state 12, tracking distances and lexicographically minimal word for each state at each distance? Actually BFS yields shortest distance; we can also store predecessor and the character used to get there, but need lexicographically minimal among all shortest paths. Since BFS explores edges in order of alphabet? If we do BFS where we enqueue neighbors in alphabetical order, the first time we reach target state will be via lexicographically smallest shortest path? Not necessarily: BFS ensures shortest distance; if we process nodes in FIFO order and for each node we explore outgoing edges in alphabetical order, then the first time we discover the target state will be via the lexicographically smallest among all shortest paths? Let's think.

Standard BFS on unweighted graph where each edge has a label (character). We want the lexicographically smallest string among all shortest paths from source to target. If we do BFS layer by layer, and within each layer we process nodes in the order they were discovered (which depends on previous layer's ordering), and for each node we consider outgoing edges in alphabetical order, then the first time we reach target will be via lexicographically smallest string among shortest paths. Reason: BFS explores all strings of length L in lexicographic order if we use a queue that processes nodes in the order they were discovered and we expand edges in alphabetical order. Actually, this is akin to performing a lexicographic BFS (like using a priority queue where priority is (length, string)). But using a simple queue with alphabetical edge order yields that the discovered paths are in lexicographic order within each length? Let's verify.

Consider source s. At distance 0: we have s (empty string). At distance 1: we consider all outgoing edges from s in alphabetical order, enqueue the resulting states with the corresponding strings (single char). The queue will have those states in order of the characters: first all states reachable by 'a' (in the order they are discovered from s via 'a'), then those via 'b', etc. However, if multiple edges lead to same state, we may discover it earlier via a smaller char; but we only mark visited when first discovered, so we will not consider alternative longer or same length paths to same state later. This could affect lexicographic minimality: Suppose there are two different shortest paths to target of same length, but the first discovered path (via BFS) may not be lexicographically smallest because the node leading to target via a larger char may be discovered earlier due to earlier discovery of its predecessor via a different path. Example: Suppose we have two paths of length 2: "ba" and "ab". Both length 2. Lexicographically smallest is "ab". BFS from source: At distance 1, we discover states via 'a' then 'b'. Suppose the state after 'a' leads via 'b' to target (path "ab") and the state after 'b' leads via 'a' to target (path "ba"). If we process distance 1 nodes in order: first the node reached by 'a' (state A), then node reached by 'b' (state B). When we expand state A, we consider its outgoing edges in alphabetical order: 'a' then 'b' etc. If from A, the edge 'b' leads to target, we will discover target via "ab" when processing A's 'b' edge. Then we will mark target visited and stop (if we stop upon first discovery). That yields "ab", which is lexicographically smallest. Good.

But consider scenario where the lexicographically smallest path uses a first character that is not the smallest possible first character among all shortest paths? Actually, if there is a shortest path starting with 'a', then any path starting with 'b' is lexicographically larger regardless of later chars. So the lexicographically smallest shortest path will have the smallest possible first character among all shortest paths. BFS that processes edges in alphabetical order from source will discover all states reachable by 'a' at distance 1 before any state reachable by 'b' at distance 1. So if there exists a shortest path starting with 'a', the target will be discovered (if reachable via 'a' at some depth) during expansion of the 'a' frontier before any 'b' frontier nodes are processed. However, it's possible that the shortest path starting with 'a' has length L, but the target is not reached at distance 1 via 'a' but maybe later after some steps; but still all nodes at distance 1 via 'a' are processed before any distance 1 via 'b' nodes. Then their children (distance 2) are processed in order: all children of the first 'a' node, then children of second 'a' node, etc., before any children of 'b' nodes. This ensures that strings are explored in lexicographic order: all strings starting with 'a' of length L are explored before any string starting with 'b' of length L. More formally, BFS with queue and alphabetical edge order yields lexicographic order of strings (like a BFS on a trie). So first time we encounter target yields lexicographically smallest shortest string.

Thus we can do BFS from state 12, exploring outgoing edges in order a,b,c,d,e, and stop when we first reach state 6. Record the path.

We need to reconstruct the word. We'll need to keep predecessor and the character used.

Let's implement mentally or via reasoning.

We have 21 states (0-20). Let's list transitions for each state:

I'll rewrite them clearly:

State 0:
 a->15
 b->15
 c->6
 d->9
 e->18

State 1:
 a->3
 b->3
 c->5
 d->18
 e->15

State 2:
 a->15
 b->8
 c->10
 d->20
 e->0

State 3:
 a->3
 b->6
 c->10
 d->12
 e->19

State 4:
 a->1
 b->10
 c->14
 d->18
 e->16

State 5:
 a->9
 b->14
 c->13
 d->13
 e->5

State 6:
 a->18
 b->17
 c->11
 d->16
 e->17

State 7:
 a->4
 b->14
 c->19
 d->9
 e->16

State 8:
 a->12
 b->18
 c->7
 d->0
 e->5

State 9:
 a->3
 b->19
 c->4
 d->13
 e->6

State 10:
 a->16
 b->6
 c->7
 d->4
 e->0

State 11:
 a->12
 b->20
 c->9
 d->5
 e->13

State 12:
 a->1
 b->2
 c->10
 d->19
 e->9

State 13:
 a->16
 b->13
 c->0
 d->17
 e->4

State 14:
 a->11
 b->18
 c->1
 d->8
 e->10

State 15:
 a->14
 b->1
 c->20
 d->20
 e->20

State 16:
 a->12
 b->3
 c->2
 d->20
 e->13

State 17:
 a->6
 b->17
 c->3
 d->16
 e->1

State 18:
 a->5
 b->11
 c->9
 d->12
 e->6

State 19:
 a->18
 b->13
 c->7
 d->3
 e->10

State 20:
 a->15
 b->6
 c->14
 d->3
 e->7

Goal: from state 12 to state 6.

Let's BFS manually.

We'll compute distances and predecessors.

Initialize: start at 12, distance 0, word "".

We'll maintain queue.

We'll also keep visited set to avoid revisiting (since BFS first visit is shortest). We'll also need to store the word or predecessor+char to reconstruct.

Let's do BFS step by step.

We'll create a table: state -> (prev state, char used) and distance.

Start: state 12, dist 0, prev = None.

Queue: [12].

Visited: {12}.

Now process 12.

From state 12, transitions:
 a->1
 b->2
 c->10
 d->
```

