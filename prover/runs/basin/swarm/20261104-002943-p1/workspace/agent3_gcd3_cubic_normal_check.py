from sage.all import *
from pathlib import Path
R=PolynomialRing(QQ,'x');x=R.gen();G=x*(x*x-4);P=G*(x-3);Q=G*(x-4);C=QQ(1);D=P*Q-C;f=(x+1)*(x-1)*(x-QQ(5)/2);gg,gi,unused=G.xgcd(D);assert gg==1
red=lambda p:R(p).mod(D)
integ=lambda p:red(f*Q*R(p))[7]
def moment(p):return vector(QQ,[integ(p*x**j) for j in range(4)])
def gram(p):return matrix(QQ,4,4,lambda i,j:integ(p*x**(i+j)))
def vpoly(v):return sum(v[i]*x**i for i in range(4))
def jet(ws,ref):
 order=len(ws)-1;iv=gram(ws[0]).inverse();pol=[ref]
 for j in range(1,order+1):pol.append(-vpoly(iv*sum((moment(ws[k]*pol[j-k]) for k in range(1,j+1)),vector(QQ,4))))
 raw=[red(sum(ws[a]*pol[b]*pol[j-a-b] for a in range(j+1) for b in range(j-a+1))) for j in range(order+1)];den=[integ(p) for p in raw];out=[]
 for j in range(order+1):out.append(red((raw[j]-sum(den[k]*out[j-k] for k in range(1,j+1)))/den[0]))
 return out
Ninv=gram(P*P/C).inverse();points=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1),(1,1,1)]
results=[]
for co in points:
 ell=sum(co[j]*x**j for j in range(3));rr=red(gi*ell);eta=-rr;out=jet(jet([R.one(),eta,R.zero(),R.zero()],P),Q);assert red(out[1]-eta)==0 and moment(P*out[2])==vector(QQ,4)
 correction=red(out[3]+out[2]*rr);normal=Ninv*moment(P*correction)/C
 results.append((co,normal));print('co',co,'normal3',normal)
print('Allzero?',all(v==vector(QQ,4) for co,v in results))
import pickle;pickle.dump({'results':results},open('workspace/agent3_gcd3_cubic_normal.pkl','wb'))
