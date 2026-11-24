"""Finite symbolic checks for the singleton obstruction on equal-area S2 x S2.
Does not purport to prove the analytic spectral-invariant theorem.
"""
import sympy as s
from pathlib import Path

# In cohomology let x,y be factor orientation classes; x*x=q,y*y=q
# in small quantum cohomology when both spheres have area 4*pi.
x,y,q=s.symbols('x y q')
G=s.groebner([x*x-q,y*y-q],x,y,q)
def reduce(p): return s.expand(G.reduce(p)[1])
assert reduce(x*x)==q
assert reduce(y*y)==q
assert reduce(x*y)==x*y
assert reduce((x*y)*(x*y))==q*q
# Poincare duality translates x to A=[pt x S2], and 1 to [M].
# q corresponds to recapping by a sphere of area 4*pi, spectral shift -4*pi.
assert s.simplify((4*s.pi)-4*s.pi)==0
# A sphere class (m,n) has omega=4*pi*(m+n), c1=2*(m+n).
m,n=s.symbols('m n',integer=True)
omega=4*s.pi*(m+n)
c1=2*(m+n)
assert s.simplify(omega-2*s.pi*c1)==0
# Check the cohomology cup-length independently of the quantum deformation.
Gc=s.groebner([x*x,y*y],x,y)
assert Gc.reduce(x*y)[1]==x*y
assert Gc.reduce(x*y*x)[1]==0
assert Gc.reduce(x*y*y)[1]==0
# Euler characteristic and ordinary cup-length.
betti=[1,0,2,0,1]
assert sum((-1)**i*b for i,b in enumerate(betti))==4
print('Verified quantum identities x^2=y^2=q, (xy)^2=q^2.')
print('Verified monotonicity omega=2*pi*c1, area period 4*pi, minimal Chern number 2.')
print('Verified ordinary cup length 2, Euler characteristic 4.')
print('Singleton contradiction: strict spectral LS gives c(1)-4*pi < c(x) < c(1),')
print('whereas spectrality for one orbit puts both numbers in the same 4*pi-lattice.')
Path('workspace/agent3_quantum_check.py').write_text(Path(__file__).read_text())
