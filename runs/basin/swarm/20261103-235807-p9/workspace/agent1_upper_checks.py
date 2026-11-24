import sympy as sp
import numpy as np
from pathlib import Path
p=sp.symbols('p', positive=True)
q=p/(p-1)
beta=1+1/(p*(p-1))
assert sp.simplify(1/p+1/q+q/p**2-beta)==0
assert sp.simplify((1+1/(q*(q-1)))/(p-1)-beta)==0
# Check exact Holder gaps governing the two maximal operators.
r,s=sp.symbols('r s', positive=True)
a=q*s/(q*s-1)
b=p*r/(p*r-1)
assert sp.simplify(p/a-1-(p-1)*(s-1)/s)==0
assert sp.simplify(q/b-1-(q-1)*(r-1)/r)==0
# Random finite atomic weights: verify scalarization inequality for arbitrary
# directions and check matrix A_p is at least 1 (all intervals are full space).
rng=np.random.default_rng(1729)
checks=0
for pp in [1.1,1.25,1.5,1.9,2.1,3.,5.,10.]:
    qq=pp/(pp-1)
    for trial in range(30):
        atoms=[]
        for k in range(7):
            z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            h=z@z.conj().T+0.2*np.eye(2)
            vals,vecs=np.linalg.eigh(h)
            root=(vecs*vals**(1/pp))@vecs.conj().T
            atoms.append(root)
        A=np.array(atoms)
        B=np.linalg.inv(A)
        K=np.array([[np.linalg.norm(x@y,2) for y in B] for x in A])
        Q=np.mean(np.mean(K**qq,axis=1)**(pp/qq))
        assert Q>=1-1e-9
        for k in range(10):
            e=rng.normal(size=2)+1j*rng.normal(size=2)
            w=np.linalg.norm(A@e,axis=1)**pp
            scalarQ=np.mean(w)*np.mean(w**(-1/(pp-1)))**(pp-1)
            assert scalarQ<=Q*(1+1e-10)
            checks+=1
print('Exact symbolic identities: 4 passed')
print('Random atomic scalarization inequalities:',checks,'passed')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_upper_checks.py').write_text(Path(__file__).read_text())
