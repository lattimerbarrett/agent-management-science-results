from sage.all import *
import time
F=GF(1000003)
def calc(g,bs):
 r=(g+2)//3;k=g-r;h=2*g-2;N=4*g-4;d=2*g-1-k;Q=N//k
 B=2*h+1+d*Q;J=B+N+d*Q+1
 A=LaurentSeriesRing(F,'t',default_prec=4*(B+J+g));t=A.gen()
 sq=(1-t**(4*g+2)).sqrt()
 ai=-2*t**h/sq
 phi=sum(F(b)*t**(-(2*g-1-2*j)) for j,b in enumerate(bs)); phid=phi.derivative()
 n=N+1
 R=matrix(A,n,n);Z=matrix(A,n,n);Y=matrix(A,n,n)
 for m in range(n):
  coeff=F(1)
  for j in range((N-m)//k+1):
   if j: coeff*=-(F(m)/k+j-1)/j
   R[m+j*k,m]=t**(-m)*coeff*(k*phi)**j
 for i in range(n):
  for j in range(n):
   Z[i,j]=R[i,j]+(k*phi*R[i-k,j] if i>=k else 0)
   Y[i,j]=R[i,j]/t+((k*phi/t+phid)*R[i-k,j] if i>=k else 0)
 H=[s for s in range(B+1) if s%2==0 or s>=2*g+1]
 def dimker(T):
  m=T.nrows();ell=len(H)
  M=matrix(F,m*J,m*ell,sparse=False)
  for a in range(m):
   for i in range(m):
    if not T[a,i]:continue
    for si,s in enumerate(H):
     v=T[a,i]*t**(-s)*(sq if s%2 else 1)
     if v:
      for exp in range(int(v.valuation()),0):
       M[a*J-exp-1,i*ell+si]=v[exp]
  return m*ell-M.rank()
 po=dimker(ai*R.transpose())
 pl=dimker(ai**2*Z.transpose())
 SS=block_matrix([[ai**2*R.transpose(),ai*Y.transpose()],[zero_matrix(A,n,n),ai*Z.transpose()]])
 ps=dimker(SS)
 return po,ps,pl,po-ps+pl
if __name__=='__main__':
 for g in range(2,8):
  r=(g+2)//3
  bslist=[[int(j==i) for j in range(r)] for i in range(r)]+[[j+1 for j in range(r)]]
  for bs in bslist:
   st=time.time();print(g,bs,calc(g,bs),'time',time.time()-st,flush=True)
