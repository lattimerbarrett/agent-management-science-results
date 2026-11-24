from sage.all import *
from pathlib import Path
R=PolynomialRing(QQ,'x');x=R.gen();G=x*(x*x-4);P=G*(x-3);Q=G*(x-4);C=QQ(1);D=P*Q-C;f=(x+1)*(x-1)*(x-QQ(5)/2);gg,gi,unused=G.xgcd(D);assert gg==1
def red(p):return R(p).mod(D)
def integ(p):return red(f*Q*R(p))[7]
def moments(poly):return vector(QQ,[integ(poly*x**j) for j in range(4)])
def gram(weight):return matrix(QQ,4,4,lambda i,j:integ(weight*x**(i+j)))
def vpoly(co):return sum(co[j]*x**j for j in range(4))
def jet(ws,ref):
 M=gram(ws[0]);aa=-vpoly(M.inverse()*moments(ws[1]*ref));bb=-vpoly(M.inverse()*moments(ws[2]*ref+ws[1]*aa));ps=[ref,aa,bb];raw=[]
 for i in range(3):
  raw.append(red(sum(ws[a]*ps[b]*ps[i-a-b] for a in range(i+1) for b in range(i-a+1))))
 den=[integ(v) for v in raw];out=[]
 for i in range(3):out.append(red((raw[i]-sum(den[j]*out[i-j] for j in range(1,i+1)))/den[0]))
 return out
M=gram(R.one());N=gram(P*P/C)
for ell in [R.one(),x,x*x,1+x+x*x]:
 rr=red(gi*ell);eta=-rr;out=jet(jet([R.one(),eta,R.zero()],P),Q);assert red(out[0]-1)==0 and red(out[1]-eta)==0
 a2=vpoly(M.inverse()*moments(P*rr*rr));Ez=integ(P*P*rr*rr)/C;pred=red(-2*rr*rr+2*Q*a2/C+2*Ez)
 assert red(out[2]-pred)==0
 assert moments(P*out[2])==vector(QQ,4) and integ(out[2])==0
 assert integ(2*P*P*rr*rr*out[2]+P*P*out[2]*out[2])==0
 print('Hidden phase/zero-normal/negative-gradient identity checked exactly for ell=',ell)
print('All partial-gcd hidden quadratic phase identities PASS.')
