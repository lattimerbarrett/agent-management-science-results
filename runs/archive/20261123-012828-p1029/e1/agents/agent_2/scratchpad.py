from pathlib import Path
code='''import sympy as sp
X=sp.Matrix([[0,1],[1,0]])
Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
Z=sp.diag(1,-1)
I=sp.eye(2)
def tensor(parts):
    out=sp.ones(1,1)
    for a in parts:out=sp.kronecker_product(out,a)
    return out
count=0
for n in range(1,6):
    gam=[]
    for k in range(n):
        gam += [tensor([Z]*k+[S]+[I]*(n-k-1)) for S in (X,Y)]
    E=sp.eye(2**n)
    for g in gam:
        assert g.conjugate().T==g and g*g==E
        assert sp.trace(g)==0
    for j,g in enumerate(gam):
        for h in gam[j+1:]:
            assert g*h+h*g==sp.zeros(2**n)
            assert (g+h)**2==2*E
            count+=1
assert sp.Rational(9,5)**2>2
print(f'{count} exact Clifford pair tests passed; (2*0.9)^2>2 checked rationally.')
'''
Path('workspace/agent2_state_space_ccc_checks.py').write_text(code)
exec(compile(code,'agent2_state_space_ccc_checks.py','exec'))
