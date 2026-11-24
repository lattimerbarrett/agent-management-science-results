# Agent 4: rigorous auxiliary lemmas and gap audit

## Projection normality (complete argument from standard finite projection dimension)

Let M be a finite AW*-factor and D its faithful normalized continuous projection
dimension. We use the standard dimension identities
D(p join q)+D(p meet q)=D(p)+D(q), faithfulness, and
D(sup_i p_i)=sup_i D(p_i) for increasing projection nets.

Suppose projections p_i increase with projection join p, and x=x* is any upper
bound for all p_i. Put q_i=1-p+p_i. Then q_i is a projection, D(q_i) tends to 1,
and

    q_i (x-p) q_i = q_i (x-p_i) q_i >= 0.

If x-p were not positive, its spectral projection
r=1_(-infinity,-epsilon](x-p) would be nonzero for some epsilon>0. Hence D(r)>0.
Choose i with D(q_i)>1-D(r). Dimension modularity gives
D(r meet q_i)>=D(r)+D(q_i)-1>0. Let e=r meet q_i. Then

    0 <= e(x-p)e <= -epsilon e,

impossible because e is nonzero. Therefore x>=p: the projection join is also
the least upper bound in the entire self-adjoint order.

The algebraic identities are checked exactly (not numerically) in
`agent4_normality_checks.py`.

THIS DOES NOT, WITHOUT AN ADDITIONAL THEOREM, ESTABLISH GENERAL MONOTONE
SEQUENTIAL COMPLETENESS.

## Ordered finite-spectrum equidistribution rigidity

Suppose 0<=a<=b and a,b have the same finite spectral values
lambda_1>...>lambda_k, and corresponding spectral projections have the same D.
Let p,q be their respective top spectral projections. Then

    lambda_1 p = p a p <= p b p <= lambda_1 p.

Thus p(lambda_1-b)p=0. Positivity gives (lambda_1-b)^(1/2)p=0,
so bp=lambda_1 p, hence p<=q. Equal dimension and faithfulness give p=q.
This projection reduces both a and b; pass to its complement and induct.
Consequently a=b.

Norm approximation alone does not extend this proof: rounding to a grid
creates an order error of the same size as the spectral gaps.

## An invalid shortcut, with rigorous obstruction

Assume, hypothetically, that for every pair of positive A,B in M_2(M),

    q_2((A+B)^2) >= q_2(A^2)+q_2(B^2).

Then q is linear. To see this, fix arbitrary self-adjoint
H=[[a,z],[z*,b]], set K=[[0,-z],[z*,0]], and U_t=exp(K/t). For sufficiently large t,

    A_t=U_t diag(t+a,0) U_t* >=0,
    B_t=diag(0,t+b) >=0,
    A_t+B_t=tI+H+O(1/t).

Scalar-shift linearity, unitary invariance and norm continuity of q_2 imply
that the hypothetical inequality, after subtracting 2t^2 and dividing by 2t,
gives q_2(H)>=q(a)+q(b). Apply the same construction to -H to get equality.
Finally conjugate diag(x,y) by the scalar Hadamard unitary. Its diagonal corners
are both (x+y)/2, so this diagonal additivity forces q(x+y)=q(x)+q(y).

The formal noncommutative leading-order construction is checked by
`agent4_square_obstruction.py` (8 exact coefficient assertions).

This rules out treating the displayed q-of-square inequality as an elementary
weak substitute for trace additivity. It does NOT rule out the genuinely weaker
scalar-value inequality q(a+b)^2>=q(a)^2+q(b)^2, which remains unproved here.


## Conditional normal-amplification theorem (order only)

Suppose M is the e00 corner of a normal AW* algebra N, and N contains matrix
units eij (i,j>=0) such that sum_{i>=1} eii has projection join E=1-e00.
Here normal means increasing projection joins are their SA suprema. No
quasitrace normality is assumed.

Then every sequence d_i>=0 in M with bounded finite sums has an SA sum in M.
After scaling assume every finite sum is <=1. Let E_k=sum_{1<=i<=k} eii and
let T_k:E_k->e00 be the finite row [sqrt(d_1),...,sqrt(d_k)], so ||T_k||<=1.
Let P_k be its graph projection in the E_k+e00 corner, ordering domain first.
The graphs are compatible, hence P_k increases. Let P be their projection join.
By normality it is also their SA join.

Each graph contraction satisfies

    (P_k)11 >= E_k/2,
    P_k <= 2 E + (2/3)e00.

Thus P11>=E/2 and P22<e00. (The first inequality follows by compressing P>=P_k
and using the SA supremum of E_k.) In particular P11 is invertible in ENE.
Projection block identities show that

    r=P22-P21 P11^(-1) P12

is a projection, and 0<=r<=P22<e00, hence r=0. Therefore P is the graph of
T=P21 P11^(-1). The displayed weighted bound implies ||T||<=1. Compatibility
gives T E_k=T_k.

Finally TT* is the SA supremum of T E_k T*. This uses the existing-supremum
compression lemma proved by agent2: compression by any fixed element preserves
the SA supremum of a bounded increasing projection net. Since
T E_k T*=sum_{i<=k}d_i, the claim follows.

WARNING: the existence of such a NORMAL AW* amplification of a general finite
AW* M is not proved here. Usual selfdual-module constructions may assume the
very monotone completeness sought. This lemma cannot be used unconditionally.
