from sage.all import *
from sage.libs.gap.libgap import libgap

def case(m,N,p):
 F=GF(p);d=m*N
 I=identity_matrix(F,d)
 Ds=[];Es={}
 for i in range(m):
  a=copy(I)
  for k in range(N-1):a[k*m+i,(k+1)*m+i]=1
  Ds.append(a)
 for i in range(m):
  for j in range(m):
   if i==j: continue
   a=copy(I)
   for k in range(N-1):a[k*m+i,(k+1)*m+j]=1
   Es[i,j]=a
 G=libgap.Group([libgap(a) for a in Ds+list(Es.values())])
 D=libgap(Ds[0]); A=libgap(Es[1,0]);B=libgap(Es[0,1]**-1)
 comm=lambda a,b:a*b*a**-1*b**-1
 w=comm(D,comm(A,B))
 L=libgap.LowerCentralSeries(G)
 print('case',m,N,p,'order',G.Size(),'LCS orders',[x.Size() for x in L],flush=True)
 print('w3 trivial',w==libgap.One(G),'in gamma4',libgap.In(w,L[3]) if len(L)>3 else 'class<3',flush=True)
for m in [2,3]:
 for p in [2,3]:
  case(m,6,p)
