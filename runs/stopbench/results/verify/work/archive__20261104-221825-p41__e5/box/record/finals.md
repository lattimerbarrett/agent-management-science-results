# agent_1: last reply

The self-contained proof of \(b(d,k)\le d-2\) is complete and recorded in `workspace/agent2_upper_dminus2_proof.md`, with an executable construction and exact checks.

The team has not proved the sharper small-\(k\) upper bound or any sharp lower bound. No claim of the requested equality is justified yet.

# agent_2: last reply

Proved the self-contained universal bound
\[
b(d,k)\le d-2\qquad(d\ge3,\ k\ge1).
\]

This matches the requested upper bound when \(d=3\) or \(k\ge d-1\). Proof and constructive checker:
- `workspace/agent2_upper_dminus2_proof.md`
- `workspace/agent2_upper_dminus2.py`

Also proved and implemented:
- preservation under full-boundary facet addition;
- cone-saturation lemma;
- facetwise near-cone construction;
- zero-extra completion for vertex-decomposable complexes;
- one-extra completion when the original ridge skeleton is vertex-decomposable.

Checks include **14,412 constructed facet additions** and **9,122,880 full-boundary additions**, using exact recursive decomposability tests.

The sharp \(k-1\) upper cap and every requested lower bound remain unproved. No valid obstruction was found; I have not asserted the prescribed equality as established.

# agent_3: last reply

My lower-bound work did not produce a valid obstruction.

Verified contributions:
- A necessary and sufficient condition for appending a facet to a shelling: its intersection with the existing complex is pure of codimension one.
- Consequently, for \(k\ge d\), the proposed positive lower bound requires a counterexample to Simon’s extendable-shellability conjecture.
- Lower-bound obstructions transfer under coning, by taking links throughout any proposed completion.
- Exact randomized computations: 5,000 shelling-growth trials for \(d=3\) on ten vertices all completed the full skeleton. This is evidence only, not a universal result.

Executable checker: `workspace/a3_shelling_search.py`.

The general lower bound remains unproved; the team must not present the requested equality as established.

# agent_4: last reply

Established and checked:

- For \(k\ge d\), pure \(k\)-decomposability is equivalent to shellability.
- If adding one facet to a pure complex produces a shellable complex, the attachment intersection must be pure of codimension one. Hence every shelling of the original complex extends across that facet.
- Consequently, for \(k\ge d\), the assertion \(b(d,k)=0\) is equivalent to extendable shellability of every \(d\)-skeleton of a simplex. In particular, the requested lower bound \(b(3,3)\ge1\) requires a counterexample to the dimension-three case of Simon’s conjecture.

Files shared:
- `workspace/agent4_simon_reduction.md`: complete proofs of these reductions.
- `workspace/exact_decomp_a4.py`: exact recursive decomposability and shellability checkers, exhaustively checked on 1,117 small pure complexes.

No lower-bound obstruction was established. The requested exact formula therefore remains unproved by this work; the computational searches are not evidence sufficient to claim it.