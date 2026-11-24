import sympy as s
r,t,C,D=s.symbols('r t C D',positive=True)
n,ss=s.symbols('n ss',positive=True)
alpha=-ss-1
assert s.simplify(alpha*(alpha+n)+(ss+1)*(n-ss-1))==0
for N,S in [(7,3),(7,2)]:
 print('n,s=',N,S,'-Delta radial coefficient=',S*(N-2-S),'normal coefficient=',(S+1)*(N-S-1))
# Residual exponents for n7 p=9/5, U~r^-5, Phi2~r^-4,Phi3~r^-3.
p=s.Rational(9,5)
assert -5*(p-2)-8==-7
assert -5*(p-2)-7==-6
assert -5*(p-2)-6==-5
print('Subquadratic n7 nonlinear residual decay exponents checked')
