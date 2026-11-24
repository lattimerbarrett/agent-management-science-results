"""Exact lower-bound and Catalan parity verification. No external processes."""
from math import comb
from pathlib import Path

def valuation2(n):
    assert n > 0
    return (n & -n).bit_length()-1

def check(s):
    assert s >= 3
    j = 2**s-2
    D = 3*(2**(s-1))-3
    assert 2*D == 3*j
    assert all(2*d < 3*j for d in range(1,D))
    n=j//2
    central=comb(2*n,n)
    cat=central//(n+1)
    assert central%(n+1)==0
    assert valuation2(central)==s-1
    assert valuation2(n+1)==s-1
    assert cat%2==1
    # Lattice path reflection: Catalan difference, useful for upper bound.
    assert cat==comb(2*n,n)-comb(2*n,n-1)
    return (s,j,D,valuation2(central),cat%2)

if __name__=='__main__':
    for s in range(3,16):
        print(check(s))
    Path('workspace').mkdir(exist_ok=True)
    Path('workspace/check_lower_agent4.py').write_text(Path(__file__).read_text())
    Path('workspace/lower_bound_agent4.txt').write_text(r'''Let j be positive and d positive with 2d<3j. Choose j pairwise disjoint closed intervals I_i of positive length on the real line. Let gamma(t)=(t,t^2,...,t^d), and let nu_i be the image under gamma of normalized Lebesgue measure on I_i. Let mu_i^epsilon=nu_i * rho_epsilon, where rho_epsilon is normalized Lebesgue measure on the closed d-ball of radius epsilon. These are absolutely continuous Borel probability measures.
Suppose, contrary to the desired lower bound, that for every epsilon=1/n the j measures mu_i^epsilon admit a common two-hyperplane quartering. Orient each hyperplane, and write its equation b+a.x=0 with (b,a) normalized to length 1 in R^{d+1}. Compactness gives a subsequence along which both coefficient vectors converge to (b_r,a_r) in S^d, r=1,2. The corresponding polynomials p_r(t)=b_r+sum_{k=1}^d a_{rk}t^k are nonzero polynomials, since their coefficient vectors have length 1. They therefore have only finitely many real roots. Couple mu_i^{1/n} to (t,u) by x=gamma(t)+u/n, with t uniform on I_i and u uniform on the unit ball. Away from the finitely many t where p_1(t)p_2(t)=0, the signs of both approximating affine equations converge pointwise to the signs of p_1(t),p_2(t). Dominated convergence shows that all four sign patterns of (p_1,p_2) have nu_i-measure 1/4, for each i.
If I_i contained at most two distinct roots of p_1p_2 in its interior, then deleting those roots would leave at most three open subintervals, on each of which both signs are constant. At most three sign patterns could have positive measure. Hence each I_i contains at least three distinct roots in its interior. The intervals are disjoint, so p_1p_2 has at least 3j distinct real roots. This contradicts deg(p_1p_2)<=2d<3j. Consequently some n gives an absolutely continuous counterexample in dimension d. In particular for j=2^s-2 this proves D_s>=3*2^{s-1}-3.
''')
