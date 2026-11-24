from sage.all import RealBallField, QQ
import time
F=RealBallField(4096)
def mul(p,q):
 a=[F(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):a[i+j]+=x*y
 return a
def power(p,n):
 a=[F(1)]
 for _ in range(n):a=mul(a,p)
 return a
def rat(d,r):
 d,r=F(d),F(r);return r/(d+(d*d+r*r).sqrt())
def cert(a,L,H,U,R):
 eps=QQ(1)/10**8
 xs=[rat(-L-j*eps,1) for j in range(a)]
 ys=[rat(H-L-j*eps,R) for j in range(a)]
 us=[rat(U+j*eps,1) for j in range(a)]
 vs=[rat(U-H+j*eps,R) for j in range(a)]
 q=rat(H,R-1)
 PA=[F(1)];PB=[F(1)]
 for x,y,u,v in zip(xs,ys,us,vs):
  PA=mul(mul(PA,[x,F(1)]),[F(1),u])
  PB=mul(mul(PB,[y,F(1)]),[F(1),v])
 PA=mul(PA,[F(1),-q]);PB=mul(PB,[q,F(1)])
 W=[]
 for init in [(1,0),(0,1)]:
  w=list(map(F,init))
  for k in range(2*a):
   if k<a:
    x,y=xs[k],ys[k];A,B,C=F(1),-x-y,x*y
   else:
    u,v=us[k-a],vs[k-a];A,B,C=u*v,-u-v,F(1)
   w.append(-(A*w[k]+B*w[k+1])/C)
  W.append(w)
 A0,A1=[sum(c*w for c,w in zip(PA,ww)) for ww in W]
 B0,B1=[sum(c*w for c,w in zip(PB,ww)) for ww in W]
 fac=F(1)
 for x,y in zip(xs,ys):fac*=x*y
 d=(A0*B1-A1*B0)*fac
 print('geometry',L,H,U,R,'a',a,'D',d.numerical_approx(digits=35))
 print('is_negative',d<0,'is_positive',d>0)
 assert (d<0) if L==-30 else (d>0)
cert(64,QQ(-30),QQ(1)/10,QQ(3)/5,QQ(100))
cert(64,QQ(-1),QQ(1),QQ(2),QQ(2))
