from sage.all import RealBallField, QQ, matrix
from time import time
F=RealBallField(4096);a=b=64;eps=QQ(1)/10**8
Q=[(F(-30+i*eps),F(0)) for i in range(a)]+[(F(0),F(1)),(F(QQ(1)/10),F(100))]+[(F(QQ(3)/5+i*eps),F(0)) for i in range(b)]
P=[[F(1)] for _ in Q]
def mul(p,c,d):
 out=[F(0)]*(len(p)+1)
 for k,x in enumerate(p):out[k]+=c*x;out[k+1]+=d*x
 return out
for i in range(len(Q)):
 for j in range(i+1,len(Q)):
  dh=Q[j][0]-Q[i][0];w=Q[j][1]-Q[i][1];D=dh+(dh*dh+w*w).sqrt()
  P[i]=mul(P[i],F(1),-w/D);P[j]=mul(P[j],w/D,F(1))
t=time();M=P;sgn=1;n=len(M);d=F(1)
for k in range(n):
 pivot=max(range(k,n),key=lambda i:abs(M[i][k].center()))
 if pivot!=k:M[k],M[pivot]=M[pivot],M[k];sgn=-sgn
 p=M[k][k];assert not p.contains_zero();d*=p
 for i in range(k+1,n):
  q=M[i][k]/p
  for j in range(k+1,n):M[i][j]-=q*M[k][j]
  M[i][k]=F(0)
d*=sgn
print('time',time()-t);print(d.numerical_approx(digits=35));print('negative',d<0);print('positive',d>0);print('radius',d.rad()); print(d);assert d<0
