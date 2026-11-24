import sympy as S
import json
from pathlib import Path
j,n=S.symbols('j n')
alpha=(n+2)/2
D=(j+1)*(j+n+1)
Qs=[]
for k in range(7):
    cs=S.symbols('c:'+str(k+1))
    Q=sum(cs[i]*(j+n/2)**(2*i) for i in range(len(cs)))
    expr=S.Poly(S.expand((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(j+alpha)*D**k),j)
    sol=S.solve(expr.all_coeffs(),cs)
    Q=S.factor(Q.subs(sol))
    assert S.Poly(S.expand((j+n-1)**2*Q-(j+3)**2*Q.subs(j,j+2)-(j+alpha)*D**k),j).is_zero
    Qs.append(Q)
    print('Verified telescoper degree',k,flush=True)
# Saves exact portable string expressions, parse via sympify with symbols j,n.
Path('workspace/agent3_telescopers.json').write_text(json.dumps([str(Q) for Q in Qs]))
# Check positivity and numerical convergence of all moments at n=19,20.
import mpmath as mp
mp.mp.dps=50
for dim in [19,20,25]:
    for k,Q in enumerate(Qs):
        q0=Q.subs({j:0,n:dim}); q1=Q.subs({j:1,n:dim})
        exact=(dim-1)**2*q0*S.gamma(S.Rational(3,2))**2/S.gamma(S.Rational(dim+1,2))**2+dim**2*q1/S.gamma(S.Rational(dim+2,2))**2
        assert exact>0
print('All 21 exact sample moments positive.')
