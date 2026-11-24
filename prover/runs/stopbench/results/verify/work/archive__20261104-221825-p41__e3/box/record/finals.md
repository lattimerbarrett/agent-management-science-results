# agent_1: last reply

I have not completed the requested proof, and I cannot honestly present the asserted equality as proved.

The rigorous progress is:

\[
b(3,k)\le 1,\qquad b(d,k)\le d-2\quad(d\ge3,\ k\ge1).
\]

The general one-vertex upper bound and the lower-bound example remain missing.

### Checked constructive results

**Cone-filling lemma.** Suppose \(\Gamma\) is pure \((d-1)\)-dimensional and \(k\)-decomposable, and \(\mathcal B\) is any family of \((d+1)\)-sets satisfying \(\partial 2^F\subseteq\Gamma\) for every \(F\in\mathcal B\). Then
\[
a*\Gamma\ \cup\ \bigcup_{F\in\mathcal B}2^F
\]
is \(k\)-decomposable.

This follows by induction on a decomposition of \(\Gamma\): a shedding face gives the corresponding cone-filling constructions in both deletion and link. The zero-dimensional base case must allow arbitrary singleton fillings.

**Dimension-three construction.** Let \(\Gamma\) be the triangle skeleton of \(\Delta\). It has a same-vertex \(k\)-decomposable completion:

* Start with the vertices \(C\) of one tetrahedron.
* Grow \(C\) along the connected facet-adjacency graph of \(\Delta\).
* When a new vertex \(v\) occurs in a tetrahedron with three vertices already in \(C\), choose one of those vertices \(w\).
* For each missing edge \(vu\), \(u\in C\), add the triangle \(vuw\). Its unique minimal new face is the edge \(vu\), so it is a valid shedding-face extension because \(k\ge1\).
* All edges on \(C\cup\{v\}\) are now present. Add the remaining triangles there by full-boundary extensions, which preserve \(k\)-decomposability.

Adding apex cones over these triangles, using the cone-filling lemma, reaches the full apex star. Every remaining original tetrahedron can then be added while preserving vertex-decomposability.

Recursively applying this construction to the ridge skeleton, with a separate outer apex, gives the weaker all-dimensional bound \(d-2\).

### Executed Python checks

The workspace contains actual implementations and recursive certificate verifiers:

| File | Executed verification |
|---|---|
| `workspace/agent1_filling.py` | 8,719 exhaustive cone-filling instances |
| `workspace/agent1_upper_d3.py` | 126 complete dimension-three constructions |
| `workspace/agent2_dim3_upper.py` | Explicit lifted certificates, including a non-vertex-decomposable input |
| `workspace/agent1_general_bound.py` | 65 dimension-four/five inputs and 3,229 facet additions, every intermediate certificate verified |

These computations support the stated lemmas and constructions—not the missing equality.

For the lower bound, no verified example was found. This is a substantive gap: for sufficiently large \(k\), \(k\)-decomposability is equivalent to shellability, so the required example must genuinely be a nonextendable partial shelling of a simplex skeleton. The lens-space candidates found computationally were rejected because they were not shellable. Reporting one of them as the required example, or treating solver timeouts as evidence, would be incorrect.

# agent_2: last reply

Verified contributions:

- Constructive same-vertex completion for vertex-decomposable complexes, including unused ambient vertices: `workspace/agent2_vd_complete.py`. Checked 19,034 inputs and 131,959 intermediate additions.
- Complete constructive proof of \(b(3,k)\le 1\) for \(k\ge1\), with recursively verified certificates: `workspace/agent2_dim3_upper.py`.
- Counterexample to the proposed “proper skeleton reduces decomposability parameter” lemma: `workspace/agent2_nonVD_proper_skeleton.py`.
- Exact SAT searches on 12 and 14 vertices returned `UNKNOWN` after 30 minutes each; they provide no existence or nonexistence proof.

The team has not completed the requested proof. The unresolved pieces are the one-vertex upper bound in dimensions \(d\ge4\) and an explicit lower-bound example already in dimension three.

# agent_3: last reply

Partial results established and checked:

- Adding a missing facet whose entire boundary is present preserves \(k\)-decomposability.
- A one-facet extension of a pure shellable complex is shellable only if the new facet’s intersection with the old complex is pure of codimension one.
- Consequently, the requested lower bound for \(k\ge d-1\) requires an actual nonextendable shelling—a counterexample to Simon’s conjecture—not merely a failure of a particular decomposition strategy.
- Exact exhaustive checks covered 33,790 small facet families and 131,785 one-facet extensions. Code and results are in `workspace/agent3_check.py`, `workspace/agent3_exhaustive.py`, and `workspace/agent3_results.json`.

No valid lower-bound example was found. The team proved the upper bound \(b(3,k)\le1\) and the weaker general bound \(b(d,k)\le d-2\), but neither the all-dimensional upper bound \(1\) nor the required lower-bound construction is complete. I cannot honestly present these partial results as a proof of the asserted answer.

# agent_4: last reply

Checked computational deliverables are in `workspace/`:

- `agent4_fastcert.py`: exact recursive \(k\)-decomposability checker, cross-validated on 67,580 cases.
- `agent4_eligibility_check.py`: 243,700 exhaustive checks of the tetrahedron-attachment criterion.
- `agent4_shelling_sat_optimized.py`: exact search encoding; no shelling trap exists on eight vertices according to the solver. Larger searches timed out.
- `agent4_600cell.json` and contraction files: locally flag PL \(3\)-sphere candidates; none yielded the required obstruction.

The team has proved the upper bound for \(d=3\), and the weaker general upper bound \(b(d,k)\le d-2\). The general one-vertex upper bound and an explicit lower-bound obstruction remain unproved. Consequently, we do **not** yet have a complete proof of the requested equality.