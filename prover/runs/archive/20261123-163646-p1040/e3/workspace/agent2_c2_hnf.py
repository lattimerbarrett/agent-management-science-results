import json,itertools,numpy as np
from scipy.sparse import csr_matrix
from pathlib import Path
class Span:
 def __init__(self):self.rows={};self.queue=[]
 def add(self,v):
  v=v.copy()
  while np.any(v):
   assert np.max(np.abs(v))<2**50
   j=int(np.flatnonzero(v)[0])
   if j in self.rows:
    r=self.rows[j];q=int(v[j])//int(r[j]);v-=q*r
    if v[j]:
     self.rows[j]=v.copy();self.queue.append(v.copy());v=r.copy()
   else:
    if v[j]<0:v=-v
    self.rows[j]=v;self.queue.append(v);return True
  return False
results=json.load(open('workspace/agent2_true_relations.json'))
for data in results:
 n=data['n'];names=data['names'];m=len(names);pairs=list(itertools.combinations(range(m),2));pi={v:k for k,v in enumerate(pairs)};d=len(pairs)
 canon={};bas=[]
 for z,lab in enumerate(names):
  if lab[0]=='K':
   _,i,j=lab;i-=1;j-=1;a,b=sorted([i,j]);s=1 if j<i else -1
  else:
   _,i,a,b=lab;i-=1;a-=1;b-=1;s=1
  canon[i,a,b]=(z,s);bas.append((i,a,b,s))
 maps=[]
 for a,b in [(i,i+1) for i in range(n-1)]+[(i+1,i) for i in range(n-1)]:
  A=np.eye(n,dtype=np.int64);Ai=A.copy();A[b,a]+=1;Ai[b,a]-=1
  T=np.zeros((m,m),dtype=np.int64)
  for z,(i,j,k,s) in enumerate(bas):
   for t in range(n):
    for u in range(n):
     for v in range(u+1,n):
      coef=s*Ai[i,t]*(A[u,j]*A[v,k]-A[v,j]*A[u,k])
      if coef:
       zz,ss=canon[t,u,v];T[zz,z]+=coef*ss
  rr=[];cc=[];vv=[]
  for c,(i,j) in enumerate(pairs):
   for u in np.flatnonzero(T[:,i]):
    for v in np.flatnonzero(T[:,j]):
     if u!=v:rr.append(pi[min(u,v),max(u,v)]);cc.append(c);vv.append(int(T[u,i]*T[v,j])*(1 if u<v else -1))
  maps.append(csr_matrix((vv,(rr,cc)),shape=(d,d),dtype=np.int64))
 S=Span()
 for i,j,k,sgn in data['relations']:
  v=np.zeros(d,dtype=np.int64)
  for x,y,c in [(i,j,1),(i,k,sgn)]:
   if x!=y:v[pi[min(x,y),max(x,y)]]+=c*(1 if x<y else -1)
  S.add(v)
 q=0
 while q<len(S.queue):
  v=S.queue[q];q+=1
  for A in maps:S.add(A@v)
 print('n',n,'GL saturation rank',len(S.rows),'needed',data['needed'],'pivot coefficients',sorted(set(int(v[j]) for j,v in S.rows.items())),flush=True)
 data['GL_rank']=len(S.rows)
Path('workspace/agent2_GLrel_results.json').write_text(json.dumps(results))
