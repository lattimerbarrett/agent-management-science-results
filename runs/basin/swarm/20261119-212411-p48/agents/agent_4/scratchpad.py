import sympy as s
from pathlib import Path
# Fibre P^2 coordinates [z0:z1:z2], removed p=[1:0:0].
# Compact line L_t is image [u:v] -> [t*u:u:v].
t=s.symbols('t', real=True)
M=s.Matrix([[t,0],[1,0],[0,1]])
p=s.Matrix([1,0,0])
assert M.rank()==2
assert M.row_join(p).det()==1 # p not on L_t, for all t
# Point a_t=[t:1:0] on L_t tends to p as t -> infinity.
a=M*s.Matrix([1,0])
sin_squared=s.cancel(1-(p.dot(a))**2/(p.dot(p)*a.dot(a)))
assert sin_squared==1/(t*t+1)
assert s.limit(sin_squared,t,s.oo)==0
# Holomorphic immersion on each affine chart of P^1.
u,v=s.symbols('u v')
# Chart u=1: z1=1, coordinates (z0,z2)=(t,v).
assert s.Matrix([t,v]).jacobian([v]).rank()==1
# Chart v=1: z2=1, coordinates (z0,z1)=(t*u,u).
assert s.Matrix([t*u,u]).jacobian([u]).rank()==1
print('Verified: each L_t is a compact embedded P1 in P2\\{p}; a_t in L_t approaches p.')
print('sin^2(Fubini-Study distance(a_t,p)) =',sin_squared)
# Nonpositive restriction on a nonzero complex tangent line excludes positive-definite Levi.
# Spectral theorem reduction: a positive definite diagonal Hermitian form has
# positive restriction on every nonzero vector; exact Sylvester criterion is sufficient.
print('Analytic steps (properness, max principle) are proved in text, not asserted by computation.')
Path('workspace/agent4_lower_bound.py').write_text(Path('scratchpad.py').read_text())
