import sympy as s
r2,n=s.symbols('r2 n',positive=True)
m=n-1;S=1+r2
# Laplacian on harmonic angular degree l times radial f(r^2).
def lap(f,l):return 4*r2*s.diff(f,r2,2)+(2*m+4*l)*s.diff(f,r2)
def euler(f,l):return l*f+2*r2*s.diff(f,r2)
# Weight w=P_l(x)f(r^2) for scale and tangent Jacobi traces.
for l,f in [(0,(r2-1)*S**(-n)),(1,S**(-n))]:
 adj=n*f+euler(f,l)+lap(S*f,l)/(2*m)
 print(l,s.factor(adj));assert s.simplify(adj)==0
ss,eta,d=s.symbols('s eta d',positive=True)
N=2*d+ss;K=(2+eta)/ss
assert s.simplify(K*(N-2*d)/2-1-eta/2)==0
assert s.simplify(K*(N-2*d)-2-eta)==0
print('Exact source-Jacobi adjoint and scale-dominance identities passed.')
