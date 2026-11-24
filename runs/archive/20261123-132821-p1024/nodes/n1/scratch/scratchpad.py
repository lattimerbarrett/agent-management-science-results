import math
import numpy as np
P=1000003

def add(a,b,scale=1):
 c=a.copy()
 for e,v in b.items():
  c[e]=(c.get(e,0)+v*scale)%P
  if not c[e]: del c[e]
 return c

def mul(a,b,emin=-10000,emax=10000):
 c={}
 for e,v in a.items():
  for f,w in b.items():
   if emin<=e+f<=emax:c[e+f]=(c.get(e+f,0)+v*w)%P
 return {e:v for e,v in c.items() if v}

def rankmod(M):
 A=np.array(M,dtype=np.int64).copy()%P
 if A.ndim<2:return 0
 nr,nc=A.shape;row=0
 for col in range(nc):
  p=next((i for i in range(row,nr) if A[i,col]),None)
  if p is None:continue
  A[[row,p]]=A[[p,row]]
  A[row]=(A[row]*pow(int(A[row,col]),-1,P))%P
  inds=np.where(A[:,col]!=0)[0];inds=inds[inds!=row]
  for st in range(0,len(inds),100):
   ii=inds[st:st+100]; A[ii]=(A[ii]-A[ii,col,None]*A[row])%P
  row+=1
  if row==nr:break
 return row

def data(g,b,s,H,ret=False):
 r=(g+2)//3;k=g-r;h=2*g-2;N=H+h;Q=N//k;e=2*g-1
 emax=e*Q+2*h+5;emin=-e*Q-2*h-5
 phi={-(e-2*j):int(v)%P for j,v in enumerate(b) if v}
 phipow=[{0:1}]
 for j in range(1,Q+1):phipow.append(mul(phipow[-1],phi,emin,emax))
 sqrt={0:1};v=1
 for j in range(1,(emax-emin)//(4*g+2)+3):
  v=v*((pow(2,-1,P)-(j-1))%P)*pow(j,-1,P)%P
  sqrt[j*(4*g+2)]=v*((-1)**j)%P
 def decomp(F,m):
  # F = global non-H0 part + W part + H1 residual; W priority
  F=F.copy();R={}
  todo=sorted([ex for ex in F if -ex>m])
  while todo:
   exp=todo.pop(0)
   if exp not in F:continue
   v=F[exp];l=-exp
   if l<=m:continue
   if l>=0 and (l%2==0 or l>=2*g+1):
    del F[exp]
    if l%2:
     for sh,w in sqrt.items():
      if sh==0:continue
      ee=exp+sh
      if ee<=emax:
       F[ee]=(F.get(ee,0)-v*w)%P
       if -ee>m and ee not in todo:
        todo.append(ee);todo.sort()
   else:
    R[l]=v;del F[exp]
  # newly added sqrt terms always positive and hence W (m>=0 here)
  return F,R
 rows=[(n,l) for n in range(N+1) for l in range(max(1,n-H+1),h+2,2) if l%2] # fix parity
 rows=[(n,l) for n in range(N+1) for l in range(1,h+2,2) if l>n-H]
 ri={q:i for i,q in enumerate(rows)}
 sources=[(n,2*a) for n in range(H,N+1) for a in range((n-H)//2+1)]
 mat=np.zeros((len(rows),len(sources)),dtype=np.int64)
 for ci,(n0,l0) in enumerate(sources):
  # W contribution represented as t^(H-n) times local W polynomial = F (U frame)
  ws={n0:{-l0:1}}
  for n in range(n0+k,N+1,k):
   F={}
   for nn,ww in ws.items():
    j=(n-nn)//k
    if j<=0:continue
    # binom(s-nn/k,j) * k^j
    v=1
    for z in range(j):v=v*(k*s-nn-k*z)*pow(z+1,-1,P)%P
    F=add(F,mul(phipow[j],ww,emin,emax),v)
   W,R=decomp(F,n-H)
   for l,v in R.items():mat[ri[(n,l)],ci]=v
   ws[n]={ex:(-v)%P for ex,v in W.items() if v}
 if ret:return mat,rows,sources
 return rankmod(mat)

if __name__=='__main__':
 for g in range(2,16):
  r=(g+2)//3
  cases=[([1]*r,'all')]+[([int(j==i) for j in range(r)],str(i)) for i in range(r)]
  vals=[]
  for b,name in cases:
   ranks=[data(g,b,s,H) for s,H in [(0,0),(1,0),(0,2*g-2),(1,2*g-2)]]
   vals.append((name,ranks,ranks[1]+ranks[2]-ranks[0]-ranks[3]))
  print(g,vals,flush=True)
