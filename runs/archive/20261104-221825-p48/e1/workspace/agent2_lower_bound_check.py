import sympy as s
from pathlib import Path
# Chart b != 0: u=[a:b:c], line b*z0-a*z1=0.
a,b,c,t,r=s.symbols('a b c t r')
z0,z1,z2=s.symbols('z0 z1 z2')
F=b*z0-a*z1
assert s.expand(F.subs({z0:a,z1:b,z2:c}))==0
assert F.subs({z0:1,z1:0,z2:0})==b
# parameter [t:r] -> [a*t:b*t:r], embedding when b != 0
M=s.Matrix([[a,0],[b,0],[0,1]])
assert M.extract([1,2],[0,1]).det()==b
assert s.expand(F.subs({z0:a*t,z1:b*t,z2:r}))==0
# Chart c != 0: u=[a:b:c], line c*z0-a*z2=0.
G=c*z0-a*z2
assert s.expand(G.subs({z0:a,z1:b,z2:c}))==0
assert G.subs({z0:1,z1:0,z2:0})==c
N=s.Matrix([[a,0],[0,1],[c,0]])
assert N.extract([1,2],[0,1]).det()==-c
assert s.expand(G.subs({z0:a*t,z1:r,z2:c*t}))==0
print('Verified in both charts: every point of P2 minus [1:0:0] lies on a projective line avoiding [1:0:0].')
Path('workspace/agent2_lower_bound_check.py').write_text(Path(__file__).read_text())
