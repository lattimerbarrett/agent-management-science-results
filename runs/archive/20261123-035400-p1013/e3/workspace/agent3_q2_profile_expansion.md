# Exact q=2 finite-profile cycle expansion

Let |A|=m, |B|=b=m-d, with d fixed. Outside finite gadgets J_A,J_B, A is a perfect matching and B is independent; all missing cross edges form a fixed bipartite graph R on gadget vertices. Absorb a matching edge into J_A if necessary to ensure every hole endpoint lies in a gadget. Put
 delta=e(J_A)-v(J_A)/2, E=e(J_B),
 W_A=sum binom(deg_JA(u),2), W_B analogously,
 M=e(R), W_R=sum binom(deg_R(u),2),
 L_A=sum_{u in A} deg_JA(u)deg_R(u), L_B analogously.
All quantities are fixed while m tends to infinity in the appropriate parity class.

Define F_k=[z^k] exp(2z+z^{-1})=2^{k/2} I_{|k|}(2sqrt2). Then
 F_{k+1}=2F_{k-1}-kF_k, F_{-k}=2^{-k}F_k.
The leading cycle count is
 c(G) ~ m! b!/(2b) F_d.
For even total n, the unique leading-optimal imbalance is d=0; for odd n it is d=1. Indeed F_2/F_0=2-2h0<1, F_3/F_1=4-4h1<1; larger same-parity positive indices decrease by the termwise bound F_{k+2}/F_k<=4/((k+1)(k+2)), and negative indices are smaller by F_{-k}=2^{-k}F_k.
Here h0=F_{-1}/F_0=0.5631786198117114... and h1=F_0/F_1=0.8878177942322558...=1/(2h0).

For d=0 or1, write h=F_{d-1}/F_d and theta=F_{d+1}/F_d=2h-d. Up to terms independent of the finite profile,
 log c(G)=log(m!b!F_d/(2b))+ H1/m + Q/m^2+O(m^{-3}).
(The displayed H1 includes its universal constant; Q below omits its universal constant.)

For d=0:
 H1=2h delta+4h E-2M+(11h-3)/4,
 Q=(1-h-2h^2)delta^2+(4-4h-8h^2)E^2+(4-8h^2)delta E
   +(5/2-h/2-11h^2/2)delta+(-4+8h-11h^2)E
   +(h-1)W_A+4(h-1)W_B+Q_R.
For d=1:
 H1=2h delta+(4h-2)E-2M+2h-7/4,
 Q=(1-2h^2)delta^2+(6-8h^2)E^2+(4+4h-8h^2)delta E
   +(7/4+2h-4h^2)delta+(-31/2+24h-8h^2)E
   -W_A+8(h-1)W_B+Q_R.
In both cases
 Q_R=2h L_A+2theta L_B+2(theta-h-1)M-2W_R.

## Derivation without holes
Let p_F(z) count collections of vertex-disjoint internal paths on an arbitrary selected vertex subset, marking the number of path blocks by z and giving every nonsingleton path its two orientations. Set R_F(z)=z^{v(F)}p_F(1/z). The first coefficients are
 [z^0]R_F=1,
 [z^1]R_F=v+2e,
 [z^2]R_F=binom(v,2)+2e(v-2)+2e(e-1)-2W.
These identities hold for all finite graphs: selected cycles need at least three edges and do not affect these coefficients.
For the whole A-part (m-a)/2 free matching edges remain, so
 R_A(z)=(1+4z+z^2)^{(m-a)/2}R_JA(z).
On rescaling z=w/m, its logarithm is
 2w + [2delta w-(7/2)w^2]/m
    +[(-6delta-2W_A)w^2+(26/3)w^3]/m^2+O(m^-3).
Similarly
 log R_B(w/b)=w+[2Ew-w^2/2]/b
   +[(-6E-2W_B)w^2+w^3/3]/b^2+O(b^-3).

The exact alternating-block cycle formula is
 c(G)=1/2 sum_{ell>=1} [z^ell]p_A [z^ell]p_B ell!(ell-1)! - mb/2
       + (cycles wholly internal).
The correction terms are negligible to every relative asymptotic order. Set q=b-ell, u=q+d. Relative to m!b!/(2b), the factorial factor, after removing m^{-u}b^{-q}, has logarithm
 U(q,d)/m+V(q,d)/m^2+O(poly(q)/m^3),
 U=(u(u-1)+q(q+1))/2,
 V=d q(q+1)/2+[u(u-1)(2u-1)+q(q+1)(2q+1)]/12.
Combine these three formal expansions and sum coefficients. All sums reduce exactly to F_k because
 sum_q 2^{q+d-r}/((q+d-r)!(q-s)!)=F_{d+s-r},
and factorial moments of q shift the F-index. The symbolic code agent3_q2_expansion_symbolic.py performs these finite polynomial reductions. Factorial tails justify termwise expansion uniformly to any fixed order.

## Cross holes, using marked path polynomials
For u in F let q_F^u(z) count the same oriented path systems, additionally weighted by the number of external cross stubs at u: 0 if omitted or internal in its path, 1 if an endpoint of a nonsingleton path, 2 if a singleton. Its reversed polynomial satisfies
 z^v q_F^u(1/z)/R_F(z)=2[1-(1+deg_F(u))z+O(z^2)].
For a fixed cross edge uv the EXACT forced-edge cycle count is
 1/4 sum_{ell>=1} [z^ell]q_A^u [z^ell]q_B^v ((ell-1)!)^2 -1.
The subtraction removes the spurious 2-cycle on u,v. This identity was independently checked against brute-force cycle DFS on93 joined-forest examples.
Applying the first-order reversed expansions to this formula gives
 P(uv in C)=2/m+[2d-2h(1+deg_JA(u))-2theta deg_JB(v)]/m^2+O(m^-3).
For two prescribed cross edges, the probability both occur is 4/m^2+O(m^-3) if disjoint and 2/m^2+O(m^-3) if incident. Inclusion-exclusion over the fixed hole set, followed by taking logarithms, gives exactly Q_R above. Three or more holes affect only order m^-3.

## Irrationality and the precise exchange target
The Bessel recurrence gives
 h0=1/(1+2/(2+2/(3+2/(4+...)))).
Its positive generalized continued-fraction convergents have denominators q_j>=j!, and errors less than 2^j/(q_j q_{j+1}). The infinite value differs strictly from every convergent, while q_j times the error tends to zero; hence h0 is irrational (otherwise distance from its fixed rational value to the jth convergent is at least1/(Q q_j)). Therefore h1=1/(2h0) is irrational too.

The edge-profile objective is Z=delta+E-M. Put L=delta+2E.
For even n the first-order cycle objective is 2h0 L-2M. Ties force L and M separately equal; on such a tie, maximizing edges means minimizing E. Up to an additive constant depending on L,M, the second-order cycle objective becomes
 -8h0 E^2+[4h0 L+9(h0-1)]E
 +(h0-1)(W_A+4W_B)+2h0(L_A+2L_B)-2W_R.
For odd n the first-order cycle objective is 2h1 L-2(E+M). Ties force L and E+M separately equal, hence Z=L-(E+M) is equal: odd-n ties cannot sacrifice edges.

This does NOT prove the required H-specific exchange theorem. It identifies exactly which linear and quadratic functionals that theorem must control.

## Regression check
For even n=4k+2 compare primary Star9+matching, secondary independent, with primary matching+isolate and two secondary matching edges. Their first-order cycle objectives tie, whereas the latter has two fewer edges. The exact quadratic formula gives
 lim n^2(c_T/c_S-1)=40-56h0=8.4619972905...>0,
agreeing with exact counts for n162,322,642. Thus no arbitrary-hereditary-profile version of the missing H-specific exchange theorem is possible.
