from pathlib import Path
import sympy as s
n,k,d=s.symbols('n k d',positive=True)
q=2*(n-1)/n
# Boundary L^q radial integral root exponent.
source_growth=s.simplify((q*(k-n)+(n-1))/q)
assert s.simplify(source_growth-(k-n/2))==0
# Taylor remainder k=d+1, coefficient eps^d, radius r/eps.
assert s.simplify(d-(d+1-n/2)-(n-2)/2)==0
# source-outer cross relative to a_k eps^((n-2)/2)
assert s.simplify(n-2-(k-1)-(n-2)/2-(n/2-k))==0
# critical boundary source H^-1/2 dyadic shell norm.
# L1(shell j) exponent = n-1-n/2 = (n-2)/2;
# kernel between separated shells contributes 2^(-(n-2) max(j,l)).
assert s.simplify((n-1-n/2)-(n-2)/2)==0
# profile weighted perturbation radial exponent.
assert s.simplify(2+2*(k-n)+(n-1)-(2*k-n+1))==0
print('All exact scaling/exponent identities passed.')
