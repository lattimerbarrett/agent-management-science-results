import sympy as S
# Fan, smoothness, wall degrees and the stated Calabi--Yau subgroup.
u=[S.Matrix(v) for v in [(0,0,1),(1,0,1),(0,1,1),(1,1,1),(2,0,1)]]
for cone in [(0,1,2),(1,2,3),(1,3,4)]:
 assert abs(S.Matrix.hstack(*(u[i] for i in cone)).det())==1
assert u[0]+u[3]-u[1]-u[2]==S.zeros(3,1)
assert u[2]+u[4]-u[1]-u[3]==S.zeros(3,1)
assert S.Matrix.hstack(u[3],u[2],u[1])*S.Matrix([1,2,-3])==S.Matrix([-2,3,0])
# The degree-three term of a transverse cylinder in the K character.
x,y,j,k,z=S.symbols('x y j k z')
cyl=(x*z-x*x*z*z/2+x**3*z**3/6)*(y*z-y*y*z*z/2+y**3*z**3/6)*(1-(j*x+k*y)*z)
assert S.expand(S.expand(cyl).coeff(z,3)+x*y*(j*x+k*y+(x+y)/2))==0
q=S.symbols('q')
H1=1/(1-q)
H2=1/((1-q)*(1-q**2))
W={(0,0):S.Integer(1),(1,0):H1,(0,1):H1,(2,0):H2,(3,0):H2,(1,1):H1**2+1/q,(2,1):H1*H2+q**-2*H1,(3,1):H1*H2+q**-1*H1}
# Independently generate the two-leg table from the Schur vertex formula.
t=S.symbols('t')
def transpose(lam):
 return tuple(sum(r>i for r in lam) for i in range(max(lam,default=0)))
def norm(lam): return sum(r*r for r in lam)
def h(r):
 return S.Integer(0) if r<0 else t**r/S.prod(1-t**(2*i) for i in range(1,r+1))
def skew(lam,eta):
 n=len(lam); eta=eta+(0,)*(n-len(eta))
 if n==0: return S.Integer(1)
 return S.det(S.Matrix(n,n,lambda i,j:h(lam[i]-eta[j]-i+j)))
parts=[(),(1,),(2,),(1,1)]
for idx,lam in enumerate(parts):
 for b,mu in enumerate([(),(1,)]):
  terms=[]
  for eta in [(),(1,)]:
   if all(i<len(lam) and eta[i]<=lam[i] for i in range(len(eta))) and all(i<len(mu) and eta[i]<=mu[i] for i in range(len(eta))):
    terms.append(skew(transpose(lam),eta)*skew(mu,eta))
  vertex=t**(-norm(lam)-norm(transpose(mu)))*sum(terms)
  assert S.cancel(vertex-W[idx,b].subs(q,t*t))==0
# 2=row(2), 3=column(2); local L and edge E
shapes=[(0,0,0,0,S.Integer(1)),(1,1,1,S.Rational(1,2),H1),(2,2,3,-S.Integer(1),H2),(3,2,3,S.Integer(4),H2)]
# Check all edge gradings and insertion constants directly from the boxes.
for sh,a,E,L,H in shapes:
 lam=parts[sh]
 boxes=[(j,k) for k,row in enumerate(lam) for j in range(row)]
 assert len(boxes)==a
 assert sum(1+j+k for j,k in boxes)==E
 assert S.Rational(a,2)-sum(2*j-3*k for j,k in boxes)==L
Z={(0,0):S.Integer(1)}; F={}
for sh,a,E,L,H in shapes:
 for b in range(2):
  if a+b==0: continue
  w=W[sh,b]; pref=(-1)**(a+b)*q**(E+b)*H*(H1 if b else 1)
  key=(a,b)
  Z[key]=S.factor(Z.get(key,0)+pref*w)
  F[key]=S.factor(F.get(key,0)-6*pref*(q*S.diff(w,q)+(L+S.Rational(b,2))*w))
for key in sorted(F):print(key,'Z=',Z[key],'F=',F[key])
R=S.factor(F[2,1]-Z[1,0]*F[1,1]-Z[0,1]*F[2,0]+(2*Z[1,0]*Z[0,1]-Z[1,1])*F[1,0]+(Z[1,0]**2-Z[2,0])*F[0,1])
p=S.symbols('p')
print('R(q)=',R)
print('R(p)=',S.factor(R.subs(q,-p)))
print('series=',S.series(R.subs(q,-p),p,0,12))
# Formal bivariate division, independent of the displayed hand formula.
G={}
for key in sorted(F,key=lambda x:(sum(x),x)):
 a,b=key
 G[key]=S.factor(F[key]-sum(Z[i,j]*G.get((a-i,b-j),0) for i,j in Z if (i,j)!=(0,0) and i<=a and j<=b))
assert S.cancel(G[2,1]-R)==0
answer=-18*p**2/((1-p)*(1+p)**3)
assert S.cancel(R.subs(q,-p)-answer)==0
print('All checks passed.')
