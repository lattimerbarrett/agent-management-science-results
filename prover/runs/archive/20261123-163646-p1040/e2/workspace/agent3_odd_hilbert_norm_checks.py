import sympy as s
from pathlib import Path
x=s.symbols('x')
results=[]
for p in [3,5,7,11,13,17,19]:
 f=s.Poly(sum(s.binomial(p,j)*x**(j-1) for j in range(1,p+1)),x)
 N=int(s.resultant(f.as_expr(),1+x**(p-1),x))
 assert N%p==1 and N%(p*p)!=1
 results.append((p,N%(p*p)))
print('Cyclotomic critical Hilbert tests (p, Norm mod p^2):',results)
Path('workspace/agent3_odd_hilbert_norm_checks.py').write_text(Path(__file__).read_text())
