import sys,time,json
sys.path.insert(0,'workspace')
from agent3_enumerate import enumerate_deg
import sympy as sp
source=open(__file__).read();source='\n'.join(l for l in source.splitlines() if not l.startswith('source='));open('workspace/agent3_n10_check.py','w').write(source+'\n')
out=[]
for d in range(2,10):
 gs,c,states=enumerate_deg([d]*10);best=sp.Rational(-1);BG=None
 for G in gs:
  n=G.order();L=sp.zeros(n)
  for i in range(n):
   L[i,i]=d
   for j in G.neighbors(i):L[i,j]=-1
  hit=sp.zeros(n)
  for t in range(n):
   ix=[i for i in range(n) if i!=t]
   Q=L.extract(ix,ix).inv();h=Q*sp.ones(n-1,1)*d
   for a,i in enumerate(ix):hit[i,t]=h[a]
   for a,i in enumerate(ix):
    assert h[a]==1+sum((hit[j,t] if j!=t else 0) for j in G.neighbors(i))/d
  RQ=L.extract(list(range(1,n)),list(range(1,n))).inv()
  for i in range(n):
   for j in range(i+1,n):
    R=RQ[j-1,j-1] if i==0 else RQ[i-1,i-1]+RQ[j-1,j-1]-2*RQ[i-1,j-1]
    commute=hit[i,j]+hit[j,i]
    assert commute==n*d*R
    if commute>best:best=commute;BG=G
 rec={'d':d,'classes':len(gs),'max_tau':str(best),'edges':list(BG.edges(labels=False))}
 out.append(rec);print(rec,flush=True);json.dump(out,open('workspace/agent3_n10_certificate.json','w'))
