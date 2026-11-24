from math import comb
from fractions import Fraction

def support_fraction(m,k,t):
    """Exact fraction of t-subsets C with |A intersect C|>(t+m-2k)/2."""
    s=m-2*k
    den=comb(m,t)
    return sum((Fraction(comb(k,j)*comb(m-k,t-j),den) for j in range(max(0,t-(m-k),(t+s)//2+1),min(k,t)+1)),Fraction(0))

def lifted_density_limit(p):
    """Optimal minimum-degree fraction in the weighted 3-lift construction."""
    return p/(3*(1+p))
