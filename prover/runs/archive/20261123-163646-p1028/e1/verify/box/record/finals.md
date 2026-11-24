# agent_1: last reply

The formula is correct. A complete proof, together with the executable exact-arithmetic certificates, is supplied here:

- [Complete proof](sandbox:/Users/barrett/code/swarm_frontier/runs/archive/20261123-163646-p1028/e1/workspace/complete_certificate_agent1/PROOF.md)
- [Proof, Python sources, enumeration results, and verification log](sandbox:/Users/barrett/code/swarm_frontier/runs/archive/20261123-163646-p1028/e1/workspace/regular_graph_proof_certificate.zip)

The complete certificate was **actually run successfully**. It recomputed all proof-critical finite enumerations, rather than trusting stored tables, and finished with
```text
ALL PROOF CERTIFICATES PASSED.
```
The recorded run took approximately 44 seconds. Instructions are in `README.md`; the command is
```bash
python RUN_ALL.py
```
using Python with SageMath, NetworkX, and SymPy available. No floating-point resistance calculations, random searches, external graph generators, or downloads are used.

Below is the argument’s organization and the principal calculations. The linked proof includes the detailed cut arguments, all exceptional cases, and the enumeration-exhaustivity proofs.

## 1. Reduction to effective resistance

Write \(R_G(x,y)\) for effective resistance with unit resistances on the edges. The commute-time identity gives
\[
\mathbb E_xT_y+\mathbb E_yT_x=2|E(G)|R_G(x,y).
\]
Consequently, for a \(d\)-regular graph,
\[
\tau(G)=dn\max_{x,y}R_G(x,y).                                      \tag{1}
\]

For completeness, if \(h_y(x)=\mathbb E_xT_y\), then
\[
Lh_y=\deg-2|E(G)|e_y.
\]
Thus
\[
L(h_y-h_x)=2|E(G)|(e_x-e_y).
\]
Taking the potential difference between \(x\) and \(y\) proves the identity.

The proof uses Thomson’s principle, the resistance triangle inequality, Foster’s identity
\[
\sum_{e\in E(G)}R_G(e)=n-1,
\]
and exact solutions of grounded integer Laplacians.

## 2. The sharp cubic bound

For every connected cubic graph of even order \(n\ge10\),
\[
\max_{x,y}R_G(x,y)\le
\begin{cases}
n/2-9/4,&n\equiv2\pmod4,\\
n/2-11/4,&n\equiv0\pmod4.
\end{cases}                                                     \tag{2}
\]

Here is the bridge-block argument.

Delete all bridges. Every nontrivial remaining component is two-vertex-connected: a cut vertex in a bridgeless graph would need degree at least four. Therefore a component of order \(b\) has resistance between any two vertices at most \(b/4\), by sending current along the two arcs of a cycle containing them.

Every component separated by one bridge contains at least five vertices. Indeed, its degree sum is \(3b-1\), so \(b\) is odd, and simplicity excludes \(b=1,3\).

Fix \(x,y\) and follow their bridge-block path. Assign every off-path branch to the path block where it attaches. For a path block let \(w\) be its assigned order and \(r\) its internal resistance, and put
\[
D=\frac w2-1-r.
\]
Series resistance gives
\[
R_G(x,y)=\frac n2-1-\sum D.
\]
The following bounds hold:

- each terminal block has \(D\ge5/8\);
- a terminal block other than the five-vertex standard cap has \(D\ge9/8\);
- each internal block has \(D\ge0\);
- a nonstandard internal block has \(D\ge1/2\).

The only small resistance calculations needed are terminal caps of orders five and seven. Exhaustive exact enumeration gives respectively
\[
\frac78,\qquad\frac{11}{8}.
\]
All other cases follow from the cycle bound and the five vertices contributed by every off-path branch.

Thus \(\sum D\ge5/4\). If every block is standard, the order is \(10+4k\); hence when \(n\equiv0\pmod4\), some block contributes an additional \(1/2\). This proves (2).

Equality is attained by chains consisting of:

- two five-vertex caps, or one five-vertex and one seven-vertex cap;
- \(k\) copies of \(K_4-e\), whose two degree-two ports have resistance \(1\);
- bridges between consecutive ports.

Their orders and terminal resistances are
\[
\begin{array}{c|c}
n& R\\ \hline
10+4k&2k+11/4\\
12+4k&2k+13/4 .
\end{array}
\]
Multiplying by \(3n\) gives the two asserted even formulas.

## 3. The sharp four-regular bound

The central local estimates concern two-connected graphs with degree-two ports and all other vertices of degree four.

For a two-port graph of order \(b\),
\[
R(s,t)\le\frac{3b+2}{16}.                                        \tag{3}
\]
For a one-port graph of order \(b\),
\[
\max_vR(s,v)\le\frac{3b}{16}-\frac{13}{40}.                       \tag{4}
\]

These are proved by a maximal nested chain of two-edge cuts. Give each interlayer edge current \(1/2\). Maximality and even cut parity imply, for every subset of a layer,
\[
|\delta_A(U)|\ge |\sigma(U)|+2,
\]
where \(\sigma\) is the entering-minus-leaving incidence count. Consequently the prescribed boundary currents can be completed internally with edge currents bounded by \(1/4\).

The resulting energy estimates prove (3), except for layers of orders four and five; their exact maximum prescribed-current energies are \(1/4\) and \(1/3\). For (4), the terminal-tail calculation reduces to orders six through ten. Their exact maximum internal energies are
\[
\frac3{10},\quad\frac{73}{180},\quad
\frac{37}{70},\quad\frac{59}{90},\quad\frac{21}{20}.
\]
All these finite checks are recomputed by the certificate.

The small one-port and two-port resistance maxima are:

\[
\begin{array}{c|rrrrrrrr}
b&6&7&8&9&10&11&12&13\\ \hline
\text{one port}&
\frac45&\frac{104}{115}&\frac{36}{35}&\frac{52}{45}&
\frac{31}{20}&\frac{91}{55}&\frac95&\frac{343}{180}\\[2pt]
\text{two ports}&
\frac54&\frac43&\frac32&\frac{19}{12}&
2&\frac{25}{12}&\frac94&\frac73
\end{array}                                                     \tag{5}
\]

These are exhaustive rational computations, covering **639,086 generated degree-sequence representatives** through order thirteen. The generator’s symmetry pruning is justified in the proof; it does not discard any graph up to relabeling.

Define the defects
\[
\epsilon_b=\frac b4-R_{\rm cap},\qquad
\delta_b=\frac{b-1}{4}-R_{\rm middle}.
\]
By (3)–(4), for \(b\ge14\),
\[
\epsilon_b\ge\frac65,\qquad \delta_b\ge\frac12.
\]
These cannot improve the optimum. Orders eleven through thirteen are likewise dominated in their residue classes. Only orders six through ten remain.

If the terminal cap orders are \(a,b\) and the middle-block orders are \(b_i\), then
\[
n=a+b-1+\sum_i(b_i-1)
\]
and
\[
R=\frac n4-
\left(\epsilon_a+\epsilon_b-\frac14+\sum_i\delta_{b_i}\right).
\]
Exact min-plus optimization on the five residues gives
\[
\begin{array}{c|ccccc}
n\bmod5&0&1&2&3&4\\ \hline
\text{minimum defect}&
\frac75&\frac{23}{20}&\frac{149}{115}&\frac75&\frac{139}{90}.
\end{array}                                                     \tag{6}
\]

Branching cannot improve this: an off-path port contributes at least five additional vertices. Its defect is at least \(1\) for an internal block or \(5/4\) for an end block, exceeding every potentially competitive choice.

When no articulation separates the two marked vertices, the same cut argument gives
\[
R(x,y)\le
\max\left\{\frac n8,\frac{3n}{16}-\frac{31}{40}\right\},
\]
which is below all the required odd-order bounds for \(n\ge15\).

Therefore every four-regular graph of allowed odd order satisfies
\[
R_{\max}\le
\begin{cases}
n/4-7/5,&n\equiv0,3\pmod5,\\
n/4-23/20,&n\equiv1\pmod5,\\
n/4-149/115,&n\equiv2\pmod5,\\
n/4-139/90,&n\equiv4\pmod5.
\end{cases}                                                     \tag{7}
\]
Multiplying by \(4n\) produces precisely the four odd formulas.

## 4. Why no other degree is larger

This is essential: proving only the cubic and four-regular subclasses would not suffice.

The complete degree reductions proved in the supplied proof are summarized below. Every entry bounds \(dR_G(x,y)\).

\[
\begin{array}{c|c|c}
n&d&\text{upper bound}\\ \hline
\text{either}&2& n/2\\
\text{either}&d\ge n/2& n/2\\
\text{even}&4&\text{strictly below the cubic target}\\
\text{even}&5,6&3n/2-33/4\\
\text{even}&d\ge7&
\displaystyle
\frac{d^2+8d+3}{(d+1)(d+2)}n-d-2+\frac2{d+2}\\[4pt]
\text{odd}&6,8&n-278/45\\
\text{odd}&d\ge10&
\displaystyle
\frac{d^2+15d-8}{2(d+1)^2}n
-\frac{d^3+4d^2+15d-8}{2(d+1)^2}.
\end{array}                                                     \tag{8}
\]

For odd \(n\), regularity forces \(d\) even, so this list covers every possible degree.

Some useful details behind these reductions follow.

### Dense graphs

For \(d\ge n/2\), the complement Laplacian gives
\[
\lambda_2(L_G)\ge2d-n+2.
\]
Thus
\[
R(x,y)\le\frac2{2d-n+2},
\qquad
dR(x,y)\le\frac n2.
\]
A cycle also has commute diameter at most \(n^2/2\). Both are below the stated targets.

### Even orders, degrees five and six

The proofs use constant-width cut chains—not an assumption that arbitrary changing-width interfaces can be glued.

A useful exact flow estimate is this. Suppose a simple acyclic integer flow on \(a\) vertices has edge capacity \(C\) and total positive injection at most \(F\). In a topological ordering,
\[
\sum_e j_e\,\operatorname{length}(e)\le F(a-1).
\]
At most \(a-1\) edges have length one, so
\[
\sum_e j_e^2
 \le \frac{C(F+C)(a-1)}2.                                       \tag{9}
\]

For degree five, maximal chains of cuts of sizes two and three have matching uniform interface currents. Formula (9), the exact small tails in the certificate, and bridge reassembly give
\[
R(x,y)\le\frac{3n}{10}-\frac{33}{20}.
\]

For degree six, all cuts are even. If the marked vertices have connectivity at least four, integral quarter-capacity flow gives
\[
R(x,y)\le\frac{5(n-1)}{32}.
\]
Otherwise use a maximal two-cut chain. Ordinary layers have order at least seven and charged energy at most one quarter their order. Each terminal tail retains a defect of at least \(11/16\), giving
\[
R(x,y)\le\frac n4-\frac{11}{8}.
\]

### Even orders, degrees at least seven

Every adjacent edge has resistance at least
\[
r_0=\frac2{d+1}.
\]
If its endpoints are not closed-neighborhood twins, a four-vertex Dirichlet test improves this to
\[
r_1=\frac{2(d+1)}{d(d+2)}.
\]
There are at least \(3n/2\) nontwin edges for \(d\ge5\). Combining these lower bounds with Foster’s identity and a shortest path proves the corresponding entry in (8). Its coefficient is at most \(3/2\) for \(d\ge7\), and its constant is strictly smaller than \(-33/4\).

### Odd orders, degrees six and eight

The proof uses a valid two-level hierarchy of cuts of sizes two and four. A newly inserted four-cut must contain **all** left ports and exclude **all** right ports. Consequently unequal-width interfaces have no shared edges, and the currents \(1/2\) and \(1/4\) are consistent.

Even cut parity and maximality establish the internal transshipment capacity \(1/6\). Charging the interface energies to the atoms, and charging each isolated singleton atom to a neighboring nonsingleton atom, yields
\[
6R(x,y)\le n-\frac{278}{45},
\qquad
8R(x,y)\le n-\frac{278}{45}.
\]
The few dense atoms are exhaustively checked over \(\mathbb Q\). Endpoint estimates are proved separately; in degree eight they are entirely analytic. The full subset inequalities, charging margins, and exact dense-atom certificates are included in the proof and source bundle.

### Odd orders, degrees at least ten

Here there is a short uniform argument. In a two-connected block of order \(b\), let
\[
\Delta=\sum_v(d-\deg_Bv).
\]
A shortest cycle of length \(c\) through two specified vertices satisfies
\[
(d+1)c\le6b-10+\Delta.
\]
The reason is that its cross-chord graph has no spaced inversions and hence at most \(3(c-2)/2-2\) edges; every outside vertex has at most three neighbors on either arc.

Averaging the resistance triangle inequalities along the two arcs and using Foster’s identity gives a local block bound. Reassembling the block path, with off-path vertices paying the off-path degree deficits, gives the last entry of (8).

For \(d\ge10\),
\[
\frac{d^2+15d-8}{2(d+1)^2}\le1,
\]
because this is equivalent to \((d-1)(d-10)\ge0\). At \(d=10\) the subtracted constant is
\[
\frac{771}{121}>\frac{278}{45};
\]
for \(d\ge12\) it exceeds \(d/2+1\ge7\). Thus all these degrees are strictly below every odd target.

This completes the upper-bound half for **every** admissible graph.

## 5. Odd-order equality constructions

The four-regular extremizers are chains of explicitly supplied modules. Their checked terminal resistances are

\[
\begin{array}{c|cccc}
\text{cap order}&6&7&9&10\\ \hline
\text{root eccentricity}&
4/5&104/115&52/45&31/20
\end{array}
\]

and

\[
\begin{array}{c|cc}
\text{middle-block order}&6&8\\ \hline
\text{port resistance}&5/4&3/2.
\end{array}
\]

Ports have degree two; identifying consecutive ports makes their resulting degree four. Every other vertex already has degree four. The six-vertex middle block has a \(K_4\) core, with each port joined to a disjoint pair of core vertices.

Use the following base chains:
\[
\begin{array}{c|c}
n\bmod5&\text{base modules}\\ \hline
0&\text{cap }6,\ \text{cap }10\\
1&\text{cap }6,\ \text{cap }6\\
2&\text{cap }6,\ \text{cap }7\\
3&\text{cap }6,\ \text{middle }8,\ \text{cap }6\\
4&\text{cap }6,\ \text{cap }9.
\end{array}
\]
Insert enough six-vertex middle blocks to reach \(n\). Each insertion adds five vertices and resistance \(5/4\), so it preserves \(R-n/4\).

Series resistance gives exactly the five defects in (6). The source file `odd_construction.py` supplies every edge of every module and constructs the graph for arbitrary allowed odd \(n\). It verifies simplicity, connectivity, regularity, module resistances, and full-graph resistance diameters exactly.

Combining these constructions, the cubic constructions, (1), and all upper bounds proves
\[
\boxed{
\max_{G\in\mathcal R_n}\tau(G)=
\begin{cases}
\frac{3n(2n-9)}4,&n\equiv2\pmod4,\\[2pt]
\frac{3n(2n-11)}4,&n\equiv0\pmod4,\\[2pt]
n^2-\frac{28}{5}n,&n\text{ odd},\ n\equiv0,3\pmod5,\\[2pt]
n^2-\frac{23}{5}n,&n\text{ odd},\ n\equiv1\pmod5,\\[2pt]
n^2-\frac{596}{115}n,&n\text{ odd},\ n\equiv2\pmod5,\\[2pt]
n^2-\frac{278}{45}n,&n\text{ odd},\ n\equiv4\pmod5.
\end{cases}}
\]

The supplied complete proof and certificate contain no unresolved degree case or unproved extremal-resistance assumption.

# agent_2: last reply

Final integration is complete. All mathematical cases are proved and independently reviewed; no remaining gap was identified. The proof files and exact verification scripts are ready for the unified bundle.

# agent_3: last reply

Final polish is complete. I reran the odd constructions successfully after adding explicit assertions for every module’s resistance diameter, and removed the remaining self-copying checker code. All mathematical work and proof-critical checks are complete; the files are ready for the unified bundle.

# agent_4: last reply

All owned proof files and exact checkers are ready for the bundle. No further changes or mathematical issues found. The checkers do not modify themselves; the degree-6 tail checker writes only its result JSON.