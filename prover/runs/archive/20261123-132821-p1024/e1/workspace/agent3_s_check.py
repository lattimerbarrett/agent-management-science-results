"""Exact checks for S connecting-map vanishing in g=4,b=(0,1)."""
import sympy as s
t,q=s.symbols('t q', nonzero=True)
g=4; k=2; N=6; phi=t**-5
w=t**-1*q*(1+k*phi*q**k)**s.Rational(-1,k)
# The vertical logarithmic transition is exact.
assert s.simplify(q*s.diff(w,q)/w-1/(1+k*phi*q**k))==0
# Unique possible order-N horizontal section: its first obstruction.
ratio=(1+k*phi*q**k)**s.Rational(-N,k)
assert s.expand(s.series(ratio,q,0,k+1).removeO()).coeff(q,k)==-N*phi
# Serre pairing of phi with omega_1=x dx/z has residue -2.
omega1=-2*t**(N-2)*(1-t**(4*g+2))**s.Rational(-1,2)
assert s.residue(phi*omega1,t,0)==-2
# A has gr_n=O(np); n>=7 has H1=H0(K-np)=0.
assert all(N-n<0 for n in range(7,100))
# Exact multiplication R:H0(O(2p))->H1(O(4p)).
# Bases source=(1,x), target=(t^-7,t^-5), x=t^-2.
target=[7,5]
R=s.Matrix([[int(5+2*a==m) for a in range(2)] for m in target])
assert R==s.Matrix([[0,1],[1,0]]) and R.rank()==2
print('g=4 S obstruction: nonzero; connecting map: zero; rankR:',R.rank())
