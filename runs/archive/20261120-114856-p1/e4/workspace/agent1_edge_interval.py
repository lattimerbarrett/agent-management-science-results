import sympy as S,pickle
from pathlib import Path
from sage.all import RealIntervalField, QQ
RI=RealIntervalField(100)
data=pickle.loads(Path('workspace/agent1_exact_edge_data.pkl').read_bytes());u=data['u'];K=data['K']
R=(9*u**4-84*u**3+229*u**2-154*u-60)/(3*(9*u**4-84*u**3+229*u**2-154*u-20))
assert S.cancel(S.trace(K)-S.diff(R,u)/(2*R))==0

def add(a,b):return [a[i]+b[i] for i in range(3)]
def mul(a,b):return [sum((a[j]*b[i-j] for j in range(i+1)),RI(0)) for i in range(3)]
def inv(a):
 b=[1/a[0]]
 for i in [1,2]:b.append(-sum((a[j]*b[i-j] for j in range(1,i+1)),RI(0))/a[0])
 return b
def sqrt(a):
 b0=a[0].sqrt();b1=a[1]/(2*b0);b2=(a[2]-b1*b1)/(2*b0)
 return [b0,b1,b2]
def cRI(a):return RI(QQ(str(a)))
def polycs(expr):return [cRI(a) for a in S.Poly(expr,u).all_coeffs()]
def ratcs(expr):
 n,d=S.fraction(S.cancel(expr));return polycs(n),polycs(d)
def pj(cs,X):
 v=[RI(0),RI(0),RI(0)];xx=[X,RI(1),RI(0)]
 for c in cs:v=add(mul(v,xx),[c,RI(0),RI(0)])
 return v
def rj(cs,X):return mul(pj(cs[0],X),inv(pj(cs[1],X)))
rdata=ratcs(R);fdata=[ratcs(K[j,1]) for j in range(4)]
def evalj(j,X):return mul(rj(fdata[j],X),sqrt(rj(rdata,X)))
def certified(N):
 result=[RI(0) for _ in range(4)];h=RI(1)/N
 for k in range(N):
  X=RI(QQ(k)/N,QQ(k+1)/N);mid=RI(QQ(2*k+1)/(2*N))
  for j in range(4):
   jet=evalj(j,X);M=max(abs(jet[2].lower()),abs(jet[2].upper()))
   err=RI(-M,M)*h**3/12
   result[j]+=evalj(j,mid)[0]*h+err
 return result
for N in [64,128,256,512]:
 g=certified(N)
 print('N',N,'g',g,'widths',[float(x.absolute_diameter()) for x in g],flush=True)
 assert (g[1]+RI(QQ(3)/8)*g[2]+RI(QQ(61)/64)*g[3]).contains_zero()
print('PASS rigorous interval edge-scattering integral and exact trace factor')
