# A low-degree self-reflection interpolation obstruction

Let f be a Schur function on Re z>0 whose Pick matrices at all finite distinct
RHP nodes are strictly positive definite. If z_1,...,z_k are such nodes, then
there is NO nonzero polynomial p of degree d<k satisfying

    p(z_i)=f(z_i) p#(z_i),    p#(z)=conj(p(-conj(z))),     i=1,...,k.

No assumptions on the location of the zeros of p or p# are needed.

Proof. First remove all common zeros at interpolation nodes: if both p(z_i)
and p#(z_i) vanish, p has both roots z_i and -conj(z_i). Their product
h_i(z)=(z-z_i)(z+conj(z_i)) satisfies h_i#=h_i, so division by h_i preserves
the equations at all other nodes. Repeating t times leaves degree d'=d-2t
and k'=k-t nodes, with p# nonzero at each remaining node; still d'<k'.

Write R=p/p#. Its Pick numerator is the polynomial Bezoutian

    B(z,bar w)=[p#(z) conj(p#(w))-p(z) conj(p(w))]/(z+bar w).

The numerator vanishes at z=-bar w by the definition of #. By Hermitian
symmetry the quotient has degree at most d'-1 in each variable. Thus the
matrix [B(z_i,conj(z_j))] has rank at most d'. Dividing its rows/columns by
p#(z_i) and their conjugates shows that the Pick matrix of R on these nodes
has rank at most d'. But it agrees with the strictly positive definite k'
by k' Pick matrix of f, impossible since k'>d'. QED.

The same argument works with confluent jets, replacing finite Cauchy kernels
by their derivatives and counting total interpolation multiplicity, provided
common zero pairs and their multiplicities are removed first.

This lemma makes the desired determinant bridge weaker: it would suffice to
construct a low-degree self-reflection interpolant from singularity, even a
meromorphic quotient with poles and unstable zeros. It does NOT construct
such an interpolant from the Atiyah matrix; that step is still missing.
