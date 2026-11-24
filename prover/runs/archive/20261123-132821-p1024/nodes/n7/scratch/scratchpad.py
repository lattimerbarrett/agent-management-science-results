from sage.all import *
import time

def calc(g,bs):
 p=1000003; F=GF(p); R=LaurentSeriesRing(F,'t',default_prec=1000); t=R.gen()
 r=(g+2)//3;k=g-r;h=2*g-2;N=4*g-4;d=2*g-1-k;Q=N//k;B=2*h+1+d*Q;J=B+N+d*Q+1
 phi=sum(F(b)*t**(-(2*g-1-2*j)) for j,b in enumerate(bs));q=k*t**k*phi
 root=(1-t**(4*g+2)).sqrt();a=-F(1)/2*t**(-h)*root
 # Pinv row n col m: w^m in u coordinate
 Z=matrix(R,N+1)
 for m in range(N+1):
  c=F(1)
  for j in range((N-m)//k+1):
   if j: c*=(-F(m)/k-(j-1))/j
   Z[m+j*k,m]=t**(-m)*c*(k*phi)**j
 # inverse S = [a^-1 Z,0; H Z,E Z]
 E=identity_matrix(R,N+1);H=t**(-1)*identity_matrix(R,N+1)
 for n in range(N+1-k):
  E[n+k,n]=k*phi
  H[n+k,n]=k*phi/t+phi.derivative()
 Ainv=Z; Linv=(E*Z)/a; Sinv=block_matrix([[Z/a,zero_matrix(R,N+1)],[H*Z,E*Z]])
 funs=[t**(-s)*(1 if s%2==0 else root) for s in range(B+1) if s%2==0 or s>=2*g+1]
 ranks=[];hs=[]
 for name,Ti in [('O',Ainv),('L',Linv),('S',Sinv)]:
  m=Ti.nrows(); entries={}
  for i in range(m):
   for al in range(m):
    v=Ti[i,al]/a
    if v==0:continue
    for si,f in enumerate(funs):
     w=v*f
     for exp,coef in w.add_bigoh(0).laurent_polynomial().dict().items():
      if exp<0:
       assert exp>=-J,(g,name,exp,J)
       entries[(al*J+(-exp-1),i*len(funs)+si)]=coef
  M=matrix(F,m*J,m*len(funs),entries,sparse=True)
  rank=M.rank();ranks.append(rank);hs.append(m*len(funs)-rank)
 print('g,b',g,bs,'hO,L,S',hs,'delta',hs[0]+hs[1]-hs[2],flush=True)
 return hs

def reduced(g,bs):
 F=GF(1000003);r=(g+2)//3;k=g-r;h=2*g-2;D=h-k
 ranks=[]
 for n in range(D+1):
  rows=(D-n)//2+1;cols=n//2+1
  H=matrix(F,rows,cols,lambda l,i: bs[l+i] if l+i<r else 0)
  ranks.append(H.rank())
 RO=sum(ranks)-ranks[0]
 RA=sum(ranks)-ranks[k]
 RB=RL=sum(ranks)
 return RA-RO+RB-RL,ranks

if __name__=='__main__':
 for g in range(2,21):
  r=(g+2)//3
  out=[]
  for s in range(r):
   bs=[(j+1)**2 if j<=s else 0 for j in range(r)]
   de,rs=reduced(g,bs)
   assert de==-s
   out.append(de)
  print('reduced',g,out,flush=True)
 st=time.time();calc(7,[0,0,1]);print('time',time.time()-st,flush=True)
