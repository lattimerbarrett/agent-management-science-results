import sympy as s
e=s.symbols('e', integer=True, nonnegative=True)
def ip(D,F):
    a,b=D;c,d=F
    return s.expand(-e*a*c+a*d+b*c)
def add(D,F): return tuple(s.expand(a+b) for a,b in zip(D,F))
def mul(k,D): return tuple(k*a for a in D)
H=(1,3*e+1); P=add(mul(4,H),(0,-1))
A=(5,-1); B=(-1,12*e+5); C=add(A,B)
K=(-2,-e-2)
c2=ip(A,B)
chi=2+(ip(C,add(C,mul(-1,K))))/2-c2
print('H^2 =',ip(H,H))
print('c1 =',C,'; c2 =',c2,'; c1^2-c2 =',s.expand(ip(C,C)-c2))
print('chi(E) =',s.simplify(chi))
print('P-slopes A,B,E:',ip(A,P),ip(B,P),s.simplify(ip(C,P)/2))
print('A.S, B.f:',ip(A,(1,0)),ip(B,(0,1)))
assert C==mul(4,H)
assert s.expand(c2-13*ip(H,H))==0
assert s.expand(ip(C,C)-c2-3*ip(H,H))==0
# Exact local Levi matrix of reciprocal squared norm, for linewise diagonal
# curvature lambda_1, lambda_2, at v=(1,0) in a rank-two fibre.
x1,y1,x2,y2,u1,w1,u2,w2=s.symbols('x1 y1 x2 y2 u1 w1 u2 w2', real=True)
l1,l2=s.symbols('lambda_1 lambda_2', real=True)
G=s.exp(-l1*(x1*x1+y1*y1)-l2*(x2*x2+y2*y2))*((1+u1)**2+w1*w1+u2*u2+w2*w2)
F=1/G
pairs=[(x1,y1),(x2,y2),(u1,w1),(u2,w2)]
origin={v:0 for pair in pairs for v in pair}
M=s.zeros(4)
for i,(x,y) in enumerate(pairs):
 for j,(u,v) in enumerate(pairs):
  M[i,j]=s.simplify((s.diff(F,x,u)+s.diff(F,y,v)+s.I*(s.diff(F,x,v)-s.diff(F,y,u))).subs(origin)/4)
print('Levi(1/G) at (z,v)=(0,(1,0)) =',M)
assert M==s.diag(l1,l2,1,-1)

# Cohomology of the central split bundle: a direct summand of the
# weight-m part of H^2(U_0,O) is H^1(X, B^(m-2) tensor det(E_0)).
m=s.symbols('m', integer=True, positive=True)
a=6-m
b=(12*e+5)*m-12*e-6
k=m-6
h1=s.expand((k-1)*(b+e+1)+e*(k-2)*(k-1)/2)
print('central weight summand divisor =',a,'S + (',b,') f')
print('central weight summand h1, m >= 8 =',s.factor(h1))
for ee in range(8):
 for mm in range(8,35):
  bb=int(b.subs({e:ee,m:mm})); kk=mm-6
  direct=sum(bb+ee+t*ee+1 for t in range(kk-1))
  assert direct == h1.subs({e:ee,m:mm})
  assert direct>0
assert ip(A,H)==ip(B,H)==2*ip(H,H)

t=s.symbols('t',integer=True,nonnegative=True)
n=s.symbols('n',integer=True,nonnegative=True)
D=add(add(mul(t,A),mul(n-t,B)),C)
chi_line=1+ip(D,add(D,mul(-1,K)))/2
chi_sym=s.factor(s.summation(chi_line,(t,0,n)))
print('chi(Sym^n E tensor det E) =',chi_sym)
