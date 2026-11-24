"""Exact algebra checks for the elementary r<n uniform-bundle argument.
These are checks of bounded instances, not a proof of the full problem.
"""
import sympy as s
import json
from pathlib import Path

t=s.symbols('t')
checks=[]
for r in range(2,8):
    for k in range(1,r):
        a=s.symbols('a1:'+str(k+1))
        b=s.symbols('b1:'+str(r-k+1))
        P=1+sum(a[i-1]*t**i for i in range(1,k+1))
        Q=1+sum(b[i-1]*t**i for i in range(1,r-k+1))
        eq=[s.expand(P*Q-1).coeff(t,i) for i in range(1,r+1)]
        G=s.groebner(eq,*a,*b)
        # These are explicit ideal-membership certificates of nilpotence.
        # At every complex solution, each Chern coefficient is thus zero.
        bound=k*(r-k)+1
        for x in a+b:
            assert G.reduce(x**bound)[1]==0, (r,k,x)
        checks.append({'rank':r,'subrank':k,'nilpotence_bound':bound,'checked':True})

boundary=[]
for n in range(2,31):
    # Euler sequence: 0 -> Omega^1(1) -> O^n -> O(1) -> 0
    # on P^{n-1}. It yields a nonconstant Grassmannian map at rank n.
    P=sum((-t)**j for j in range(n))
    Q=1+t
    assert s.expand(P*Q)==1+(-1)**(n-1)*t**n
    assert s.rem(P*Q-1,t**n,t)==0
    boundary.append({'n':n,'rank':n,'product':str(s.expand(P*Q))})

result={'scope':'Exact finite algebra checks only; not the rank<2n classification.',
        'chern_ideal_checks':checks,'sharp_boundary_checks':boundary}
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_chern_checks.json').write_text(json.dumps(result,indent=2))
Path('workspace/agent1_chern_checks.py').write_text(Path(__file__).read_text())
print('Verified',len(checks),'Chern-ideal instances and',len(boundary),'Euler-sequence boundary identities.')
print('This does NOT prove uniform implies homogeneous in ranks n through 2n-1.')
print(Path('workspace/agent2_P2_proof.md').read_text())
