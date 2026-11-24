# r=2 construction (uses standard Simonovits finite-template uniqueness theorem)
Let H have vertices a_i,b_i (1<=i<=4), x,u,v and edges a_i b_i, x a_i (all i), xb_2,xb_4, ub_1,ub_2,ub_3,vb_1,vb_3,vb_4.
It has chi=3: H-x is bipartite, but xa_2b_2 is a triangle.
The following decomposition facts are explicit:
* H lies in a large complete bipartite graph with a P3 inside one class: classes B+x and A+u+v.
* H lies in such a graph with a matching of size4 in one class: classes A+B and x+u+v.
* H lies in such a graph with matchings of sizes1 and3 in the two classes: first class x,u,v,a4.
* Every two-coloring with monochromatic graphs matchings has edge-number pair exactly (4,0),(0,4),(3,1),(1,3). This finite assertion is independently checked by all 2048 assignments in agent4_r2_checks.py.
In particular complete bipartite plus two disjoint internal edges in EACH class is H-free; likewise three matching edges in only one class is H-free.

Within Simonovits D(n,2,s), the repeated connected blocks must be singletons after absorbing O(1) blocks in the exceptional set: P3 decomposition forces blocks to be matching edges or singletons, and matching4 decomposition permits only O(1) edge blocks. Each exceptional vertex sees all or none of each normal independent class. Seeing both creates H, since H-x is bipartite. Seeing neither causes a linear edge loss, while no exceptional vertex can have degree larger than n/2+O(1), and the lower bound t2(n)+4 exists. Thus every exceptional vertex sees exactly one normal class, and assign it to the opposite class. The resulting two-class graph has all cross-edges except boundedly many edges between exceptional vertices. Its internal graphs have maximum degree1 (P3 decomposition) and at most3 edges each (matching4 decomposition). Write their sizes a,b<=3 and cross deletions l. If a=3, H's (3,1) decomposition implies l>=b: otherwise some internal matching edge in the second class has all four/six requisite cross-edges to the first-class matching, yielding H, with all other vertices chosen in normal reservoirs. Thus a=3 gives surplus a+b-l<=3; similarly b=3. In all other cases surplus <=4, with equality only a=b=2,l=0. The parts must be balanced. Consequently the unique extremizer in D is balanced complete bipartite with two matching edges in each class. The standard uniqueness lifting clause gives the same unique extremizer globally for all sufficiently large n, with ex=t2+4.

For n=2m+1 let C_m=c(K_{m+1,m}). Then
C_m=((m+1)!m!/2) sum_{j=0}^{m-2}1/((m-j)j!(j+1)!).
Cycles using a fixed added internal edge in the larger/smaller class are respectively
D_A=(m-1)!m! sum_{j=0}^{m-1}1/(j!)^2,
D_B=(m-2)!(m+1)! sum_{j=0}^{m-2}1/(j!(j+2)!).
For fixed internal matchings of sizes a,b, using two or more internal edges contributes O(C_m/m^2), by the same factorial summation after contraction. Define I_j=sum_{k>=0}1/(k!(k+j)!). Then
c(a,b)/C_m=1+(2a I_0/I_1+2b I_2/I_1)/m+O(m^-2).
The edge extremizer is (a,b)=(2,2); the H-free rival (3,0) has one fewer edge but larger cycle count because
(2 I0-4 I2)/I1=4-2I0/I1>0,
using I0-I2=I1 and 1.43<I0/I1<1.44 (rigorous rational tail bounds checked in code). Thus for every sufficiently large odd n no common edge/cycle extremizer exists. This proves S2 contains0, and hence all a>=0, with C=4.

Human verification of the finite coloring assertion: Color x=0. At most one neighbor of x has color0. If none does, all a_i,b2,b4 have color1. The saturated monochromatic edges a2b2,a4b4 force u=v=0, and then b1,b3 must have color1 (otherwise either has two same-color neighbors u,v). This gives pair(0,4). If the sole color0 neighbor is a1 or a3, the same argument gives pair(1,3). If it is a2, edge a4b4 forces v=0. Were u=1, the edge ub2 would force b1=b3=0, contradicting the matching condition at v. Thus u=0 and again pair(1,3); a4 is symmetric. Finally, if the sole color0 neighbor is b2, edge xb2 forces u=1, while edge a4b4 forces v=0. The matching constraints at u and v force exactly one of b1,b3 to have color1, but that vertex then has two same-color neighbors, namely u and its matching mate a_i. This is impossible; b4 is symmetric. Interchanging colors completes the assertion.


## Fully exact comparison certificate (no asymptotic estimate needed)
The executable `agent4_r2_exact_certificate.py` proves the rival inequality for every m>=100, rather than sampling those m. For u,v selected matching edges in the two parts, contraction gives
  2^(u+v-1) sum_q binom(m+1-2u,q-u) binom(m-2v,q-v) q!(q-1)!.
The coefficient in the difference c(3,0)-c(2,2) is
  w_uv=1_{v=0} binom(3,u)-1_{u<=2}binom(2,u)binom(2,v).
After dividing by m!^2 and writing q=m-j, the summand is
  w_uv 2^(u+v-1) ((m+1-2u)!(m-2v)!/m!^2)
    * (q)_u(q)_v / [q (j+1-u)!(j-v)!].
For u+v>=1 the q quotient is a polynomial of degree <=3. Extend j to infinity, starting at j0=max(u-1,v,0). Expand the resulting polynomial in t=j-j0 in falling factorials. Since sum_{t>=0}(t)_a/[t!(t+delta)!]=I_{delta+a}, the infinite extension is a rational combination of I0,...,I4. Its rational coefficients are printed, not presumed, by the script. Their signs for m>=100 are +,-,-,-,+. Each Ij is bounded by its first20 terms and a geometric factorial tail. Clearing denominators, substituting m=100+x, and checking all polynomial coefficients nonnegative proves that this infinite extension is at least 4/(5m) for EVERY m>=100.
For the extension error, all factorial prefactors are <=1, the sum of absolute weighted coefficients is <1000, and the polynomial quotient is <=(j+5)^3 in absolute value on every extra term j>=m-2. Thus the total error is at most
  1000 sum_{j>=m-2}(j+5)^3/(j-2)!^2
  <=2000(m+3)^3/(m-4)!^2 <1/(100m).
The last inequality is checked exactly at m=100; its scaled left-hand side decreases thereafter because consecutive ratios are at most 16/(m-3)^2<1. Consequently the exact difference is positive for all m>=100. The script additionally verifies the finite contraction formula against independent join-polynomial cycle counts at m=8,10,20,50.
