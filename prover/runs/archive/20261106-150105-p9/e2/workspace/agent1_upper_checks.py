import os, sympy as sp, numpy as np
from scipy.linalg import fractional_matrix_power
p=sp.symbols('p', positive=True)
q=p/(p-1)
assert sp.simplify(1/p+1/q+q/p**2-(1+1/(p-1)-1/p))==0
assert sp.simplify((q/(q-1))-p)==0
s=sp.symbols('s', positive=True)
t=q*s/(q*s-1)
assert sp.simplify((p-t) - p*(s-1)/ (q*s-1))==0
rng=np.random.default_rng(412)
count=0
for pp in [1.2,1.5,1.9,2.1,3.,5.,10.]:
 for _ in range(50):
  def SPD():
   Z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
   return Z.conj().T@Z+np.eye(2)
  U,V,A,B=SPD(),SPD(),SPD(),SPD()
  z=rng.normal(size=2)+1j*rng.normal(size=2)
  op=lambda Z: np.linalg.norm(Z,2)
  # Directional Ap kernel inequality and Hermitian-product adjoint norm.
  assert op(U@np.linalg.inv(V))+1e-10 >=np.linalg.norm(U@z)/np.linalg.norm(V@z)
  assert np.isclose(op(A@B),op(B@A))
  assert np.isclose(op(np.linalg.inv(A)@U),op(U@np.linalg.inv(A)))
  assert op(A@np.linalg.inv(U)) <= op(A@B)*op(np.linalg.inv(B)@np.linalg.inv(U))+1e-9
  # Pairing factorization through A; np.vdot conjugates first entry.
  f=rng.normal(size=2)+1j*rng.normal(size=2)
  g=rng.normal(size=2)+1j*rng.normal(size=2)
  assert np.allclose(np.vdot(np.linalg.inv(V)@f,U@g),np.vdot(A@np.linalg.inv(V)@f,np.linalg.inv(A)@U@g))
  count+=5
print('Exact symbolic exponent / conjugacy identities: 3 passed')
print('Randomized positive-definite matrix checks:',count,'passed')
os.makedirs('workspace',exist_ok=True)
# Preserve reproducible checks as an ordinary importable script.
source=open(__file__).read()
if not __file__.endswith('agent1_upper_checks.py'):
 open('workspace/agent1_upper_checks.py','w').write(source)
