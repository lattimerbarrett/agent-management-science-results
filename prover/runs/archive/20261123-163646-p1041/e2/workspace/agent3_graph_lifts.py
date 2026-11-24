import sys,json,pathlib,time,itertools,numpy as np
sys.path.insert(0,'workspace')
_p=pathlib.Path('workspace/agent3_lift_closure.py')
_p.write_text(_p.read_text().replace('dtype=np.uint16','dtype=np.uint32'))
from agent3_lift_closure import veronese,closure
from agent1_checked_grid import degree

def kernel(S,vs):
 basis={};out=[]
 for i,s in enumerate(S):
  v=vs[s];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in basis:basis[k]=(v,c);break
   b,bc=basis[k];v^=b;c^=bc
  if not v:out.append(c)
 return out

def extendbasis(basis,v):
 while v:
  k=v.bit_length()-1
  if k not in basis:basis[k]=v;return v
  v^=basis[k]
 return 0

def nonlinear_labels(S,m,vs):
 kb=kernel(S,vs);basis={}
 for j in range(-1,m):
  l=sum(1<<i for i,s in enumerate(S) if j==-1 or s>>j&1)
  extendbasis(basis,l)
 extra=[]
 for l in kb:
  x=extendbasis(basis,l)
  if x:extra.append(x)
 return extra,len(kb)

if __name__=='__main__':
 words=json.loads(pathlib.Path('workspace/agent1_fullspan_predecessors.json').read_text())[:1]
 vs={m:veronese(m,5) for m in range(14,18)}
 start=time.time();ct=0;stats={};found=[]
 stack=[(g['support'],14) for g in words]
 while stack:
  S,m=stack.pop();extra,nu=nonlinear_labels(S,m,vs[m]);stats[(m,nu,len(extra))]=stats.get((m,nu,len(extra)),0)+1
  if m==17:continue
  assert len(extra)<=6
  for mask in range(1,1<<len(extra)):
   label=0
   for j,l in enumerate(extra):
    if mask>>j&1:label^=l
   T=[s+(((label>>i)&1)<<m) for i,s in enumerate(S)]
   cl,rk=closure(set(T),vs[m+1]);ct+=1
   if cl:
    p,c=cl[0];tt=list(set(T));hs=[p]+[s for i,s in enumerate(tt) if c>>i&1]
    F=set(hs) ^ {s+(1<<(m+1)) for s in hs} ^ {s+(1<<(m+1)) for s in T}
    assert len(F)==322
    arr=np.zeros(1<<(m+2),dtype=np.uint8);arr[list(F)]=1;assert degree(arr)<=m-5
    found.append({'graph':T,'h_support':hs,'dimension':m+2,'support':sorted(F)})
    pathlib.Path('workspace/agent3_found_graph_lift.json').write_text(json.dumps(found))
    print('FOUND',len(F),p,'at',ct);raise SystemExit
   stack.append((T,m+1))
 print('tested',ct,'stats',stats,'elapsed',time.time()-start)
 pathlib.Path('workspace/agent3_iterated_graph_lift_results.json').write_text(json.dumps({'tested':ct,'stats':{str(k):v for k,v in stats.items()},'found':found}))
 pathlib.Path('workspace/agent3_graph_lifts.py').write_text(pathlib.Path(__file__).read_text())
