"""Exact symbolic cubic shape Gram. Algebraic model only, not PDE theorem."""
import sympy as S
import json
from pathlib import Path
j,n,D,y=S.symbols('j n D y')
Qs=[S.sympify(q,locals={'j':j,'n':n}) for q in json.loads(Path('workspace/agent3_telescopers.json').read_text())]
M=[S.factor((n-1)**2*Q.subs(j,0))+S.factor(n**2*Q.subs(j,1))*y for Q in Qs]
r=[]
for k in range(4):
    rk=0
    for a in range(k+1):
        prod=S.prod(D+(s-1)*(n+1-s) for s in range(1,a+1))
        denom=S.factorial(a)*S.prod((n-1)/2-s for s in range(a))
        rk+=(-1)**(k-a)*S.binomial(k,a)*prod/denom
    r.append(S.factor(rk))
G=[]
for k in range(4):
    row=[]
    for l in range(4):
        p=S.Poly(r[k]*r[l],D)
        v=sum(c*M[mon[0]] for mon,c in p.terms())
        # Keep gamma-ratio dependence affine, factor only each coefficient.
        v=S.factor(v.subs(y,0))+S.factor(S.diff(v,y))*y
        row.append(v)
    G.append(row)
    print('Exact symbolic Gram row',k,'done',flush=True)
Path('workspace/agent3_symbolic_gram.json').write_text(json.dumps([[str(v) for v in row] for row in G]))
print('Saved symbolic Gram; y=4 Gamma((n+1)/2)^2/[pi Gamma((n+2)/2)^2].')
