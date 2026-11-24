from pathlib import Path
s=Path('workspace/agent2_boundary_functional25.py').read_text().split('# Independent direct string recursion')[0]
exec(s)
h=12;scale=pow(invdf[h-2]*fact[2*h-2]%P,P-2,P)
from sage.all import matrix,GF
import pickle,time

def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in parts(n-a,a):yield (a,)+t

def mons(d):
 return [(0,ks,e,d-sum(ks)-e) for k in range(d+1) for ks in parts(k) for e in range(d-k+1)]+[(1,ks,d-1-sum(ks),0) for k in range(d) for ks in parts(k)]

def prod(a,b):
 t,ks,e,f=a;u,ls,g,j=b
 kl=tuple(sorted(ks+ls))
 if not t and not u:return 1,(0,kl,e+g,f+j)
 if t and u:return -1,(1,kl,e+g+1,0)
 if t:t,ks,e,f,u,ls,g,j=u,ls,g,j,t,ks,e,f
 # now first open, secondtail
 if e+f:return 0,None
 return 1,(1,kl,g,0)

def integral(m):
 t,ks,e,f=m
 return onepoint(ks,e) if t else pointed(ks,e,f)
MM=[mons(d) for d in range(13)]
PP=[];bases=[]
start=time.time()
for d in range(13):
 vals=[]
 for a in MM[d]:
  row=[]
  for b in MM[12-d]:
   c,m=prod(a,b);row.append(c*integral(m)%P if c else 0)
  vals.append(row)
 Q=matrix(GF(P),vals);rows=Q.transpose().pivots();bases.append([MM[d][i] for i in rows]);PP.append(Q)
 print('degree',d,'monomials',len(MM[d]),'rank',len(rows),'time',time.time()-start,flush=True)
pickle.dump({'monomials':MM,'pairings':PP,'bases':bases},open('workspace/agent2_g12rt_pairing.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_g12rt_algebra.py').write_text(Path(__file__).read_text())
