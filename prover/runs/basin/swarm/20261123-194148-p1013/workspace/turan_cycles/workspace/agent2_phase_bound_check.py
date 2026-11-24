from fractions import Fraction as F
from math import ceil
import json
from pathlib import Path

def phasecheck(r,k):
 q=F(r-1,r);L=F(r,(r-1)*(r-2));B=F(2*r,(r-1)**2);rho=F(k-1,k);D=F((k-2)*(k-3),2*k)
 best=None;wit=None
 # n=r*m+s with m=0 formally; x=a-m, large m multiple k
 for s in range(r):
  n=s
  vals=[]
  for x in range(-2*r,2*r+1):
   z=(s-x)//(r-1);b=(s-x)%(r-1)
   ds=[F(r*x-s,r)]+[F(r*z-s,r)]*(r-1-b)+[F(r*(z+1)-s,r)]*b
   Q=sum(d*d for d in ds);cross=-Q/2
   vals.append((x,cross,Q,ds[0]))
  prof=[]
  for u in range(k):
   data=[(x,cross+x-((x-u+k-1)//k),-L*Q+4*L*rho*delta) for x,cross,Q,delta in vals]
   em=max(e for x,e,p in data);pf=max(p for x,e,p in data if e==em)
   prof.append((data,em,pf))
  for u,(df,ef,pf) in enumerate(prof):
   for v,(dg,eg,pg) in enumerate(prof):
    # offset v to have its phase MAXIMUM edge count one below F
    shift=ef-eg-1
    for x,e,p in dg:
     adv=2/q*(e+shift-ef)+p-pf+B*D
     if best is None or adv>best:best=adv;wit=(s,u,v,x,str(e+shift-ef),str(p-pf))
 pred=B*D+2*L*(2*rho-1)-2/q
 return best,pred,wit
out=[]
for r in range(3,11):
 for k in range(2,2*r+5):
  got,pred,wit=phasecheck(r,k)
  assert got==pred,(r,k,got,pred,wit)
  out.append({'r':r,'k':k,'max_advantage':str(got),'witness':wit})
 print('r',r,'checked k2..',2*r+4)
Path('workspace/agent2_phase_bound_check.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent2_phase_bound_check.py').write_text(Path(__file__).read_text())
