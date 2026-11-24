import sympy as s
import mpmath as mp
# Entire k(z)=-sum_{m>=1} z^m/(m*m!). Exact derivative-series check.
z=s.symbols('z')
for N in (4,8,16):
 K=-sum(z**m/(m*s.factorial(m)) for m in range(1,N+1))
 E=sum(z**m/s.factorial(m) for m in range(N+1))
 assert s.expand(z*s.diff(K,z)-(1-E))==0
# Uniform bound on half-plane Re(z)<=M, M>=0, a=M+1.
# On 0<t<1: (1-e^-at)/t <= a and |1-e^tz|<=1+e^M.
# On t>=1: e^-at |1-e^tz|/t <= e^-at+e^{-(a-M)t}.
M=s.symbols('M',nonnegative=True)
a=M+1
C=a*(1+s.exp(M))+s.exp(-a)/a+s.exp(-1)
assert C.is_positive
mp.mp.dps=50
def K(z):
 z=mp.mpc(z)
 if not z: return mp.mpc(0)
 if z.imag==0 and z.real<0:
  return mp.euler+mp.log(-z)-mp.ei(z)
 return mp.euler+mp.log(z)-mp.ei(z)
for zz in (1,-1,1j, -2+3j):
 val=mp.quad(lambda t: -zz if not t else (1-mp.exp(t*zz))/t,[0,1])
 assert abs(K(zz)-val)<mp.mpf('1e-40')
for MM in (0,1,2):
 aa=mp.mpf(MM+1)
 CC=aa*(1+mp.exp(MM))+mp.exp(-aa)/aa+mp.exp(-1)
 for xx in (-20,-2,0,MM):
  for yy in (-30,-5,0,5,30):
   zz=mp.mpc(xx,yy)
   error=K(zz)-mp.log(aa-zz)+mp.log(aa)
   assert abs(error)<=CC
print('PASS: exact derivative coefficients, integral identity numerics, explicit half-plane-bound tests')
print('Analytic bound: C_M=(M+1)(1+exp(M))+exp(-(M+1))/(M+1)+exp(-1), M>=0.')
