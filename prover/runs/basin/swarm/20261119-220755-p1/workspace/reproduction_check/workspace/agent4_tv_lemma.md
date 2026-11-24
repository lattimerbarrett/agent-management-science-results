# Monic-polynomial finite-variation lemma (all restart lengths)

After combining repeated eigenspaces, let the distinct active eigenvalues be
`lambda_1,...,lambda_m`, with positive initial squared spectral weights. Write
`p_{k,i}=||P_i r_k||^2/||r_k||^2`. The monic orthogonal polynomial `f_k` of degree
`s` satisfies `sum_i p_{k,i} f_k(lambda_i) lambda_i^j=0`, `0<=j<s`, and let
`N_k=sum_i p_{k,i} f_k(lambda_i)^2`. The normalized spectral-weight iteration is
`p_{k+1,i}=p_{k,i} f_k(lambda_i)^2/N_k`. An exact zero component remains zero.
Nontermination guarantees at least `s+1` support points, hence `N_k>0`.

Let `f=f_k`, `g=f_{k+1}`, `h=f_{k+2}`, `P=f*g`, `N=N_k`, `N'=N_{k+1}`.
Since `g` is monic, orthogonality of `f` gives `E_p[P]=N`.
Moreover `E_p[P^2]=N*N'`. Consequently

    E_p[(P-N)^2]=N*(N'-N),

so `N_k` increases to a finite positive limit `L`.

Put `v(x)=(1,x,...,x^(s-1))^T`, and
`M_2=sum_i p_{k+2,i} v_i v_i^T`. Since both `f` and `g` are orthogonal to
lower-degree polynomials under their corresponding weights,

    E_p[f*v]=0,       E_p[f*P*v]=0.

Thus `E_p[f*P^2*v]=E_p[f*(P-N)^2*v]`. If `c(h-f)` denotes the ascending
coefficient vector of `h-f`, its degree is below `s`, and orthogonality of `h`
at `p_{k+2}` yields the EXACT identity

    M_2 c(h-f) = -E_p[f*(P-N)^2*v]/(N*N').

All monic orthogonal polynomials here have roots in the fixed spectral hull;
their coefficients and spectral values are therefore uniformly bounded.
Also all matrices `M(p_k)` are uniformly positive definite. Indeed, the
minimum-monic norm `N(p)` is continuous on the closed simplex: it is a minimum
over a fixed compact coefficient set, because a minimizing polynomial can
always be chosen with roots in the spectral hull (including rank-deficient
weights). If a subsequence of `M(p_k)` became singular, its limiting measure
would have support at most `s-1`, and hence `N(p_k)->0`, contradicting
`N(p_k)>=N_0>0`. (In fact `N>0` excludes support at most `s`.)

Uniformly bounding the inverse of `M_2` in the exact identity gives

    ||c(f_{k+2}-f_k)|| <= C (N_{k+1}-N_k).

Therefore BOTH polynomial parities have finite total variation, and converge
to monic degree-s polynomials `f_infty,g_infty`. In particular

    ||f_{2j}-f_infty||+||f_{2j+1}-g_infty|| <= C (L-N_{2j}).

At any cluster point, equality in the norm Lyapunov identity forces the
two-block normalized residual to return to itself. Every eigenvalue in the
union of cluster supports consequently satisfies

    f_infty(lambda_i)*g_infty(lambda_i)=L.

There are at most `2s` such distinct eigenvalues. The limiting weights lie in
the one fixed affine polytope

    p>=0, sum p=1, sum p_i f_infty(lambda_i)lambda_i^j=0 (j<s).

This polynomial finite-variation lemma is independently checked over exact
rational arithmetic by `workspace/agent4_polynomial_tv_check.py`.

## Consequence when the two limiting polynomials coincide

Suppose `f_infty=g_infty=q`. If `q(lambda_i)^2>L`, the corresponding two-block
weight multiplier tends to a number greater than one, so this eigenvalue
cannot belong to the initial support and simultaneously have weight tending
to zero. Eigenvalues with `q(lambda_i)^2=L` form the limiting root set. Every
other initially active eigenvalue has `q(lambda_i)^2<L`, and its weight decays
exponentially. Orthogonality gives the exact identity

    L-N_k = E_{p_k}[(q-f_k)^2] + E_{p_k}[L-q^2].

The second term is exponentially small because it is supported off the
limiting root set. The first is at most `C||f_k-q||^2`, hence, by the tail bound,

    0 <= L-N_k <= C'(L-N_k)^2 + O(rho^k),  rho<1.

For large `k`, absorb the square term to obtain exponential norm-deficit
convergence. The strict Lyapunov inequality bounds the square of the
normalized residual's two-step displacement by a constant times
`N_{k+1}-N_k`; hence these displacements are summable, and the even residual
sequence converges. This holds for every `s`.
