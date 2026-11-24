import sys
sys.path.insert(0,'workspace')
from agent3_exact_pointed import smooth
code=open('workspace/agent2_boundary.py').read().split("print('relation matrix'")[0]
S={};exec(code,S)
P=S['P'];cols=S['cols'];idx=S['idx'];rows=S['rows'];labels=S['labels']
for row,lab in zip(rows,labels):
 r,a,b,sig,q,u,v=lab
 out=[0]*len(cols)
 for (mu,(x,y)),c in smooth(r,sig,(a,b)).items():
  m=(tuple(sorted(mu+q)),x+u,y+v)
  cc=c.numerator*pow(c.denominator,P-2,P)%P
  out[idx[m]]=cc
 assert row==out,lab
print('Independent exact source generator matches all',len(rows),'modular safe rows')
