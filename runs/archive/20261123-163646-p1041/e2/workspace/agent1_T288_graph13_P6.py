import json,sys,itertools,pathlib,time,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out

def insert(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0

def labels(S,m):
 K=kernel(S,veronese(m,5));B={}
 for j in range(-1,m):insert(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
 out=[]
 for u in K:
  r=insert(B,u)
  if r:out.append(r)
 L=[0]
 for u in out:L +=[l^u for l in L]
 return L[1:],len(K)

def reduction_basis(S,vs):
 B={}
 for j,p in enumerate(S):
  v=vs[p];c=1<<j
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
 return B

def red(v,B):
 c=0;rem=0
 while v:
  k=v.bit_length()-1
  if k not in B:rem^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return rem,c
D=json.load(open('workspace/agent4_T288_quadgraph_P16.json'));start=time.time();leaves=[];hist=collections.Counter();count=0;seen=set();hits=[]
for res in D['results']:
 for seedid,seed in enumerate(res['seeds']):
  if seed['K5']!=14:continue
  stack=[(seed['support'],11)]
  while stack:
   S,m=stack.pop();key=(m,tuple(S))
   if key in seen:continue
   seen.add(key);L,K=labels(S,m)
   if m<13:
    for u in L:stack.append(([p|(((u>>i)&1)<<m) for i,p in enumerate(S)],m+1))
    continue
   assert not L
   X,r=closure(set(S),veronese(m,3));hist[len(X)]+=1;leaves.append({'support':S,'cl3extra':[p for p,c in X]})
   if len(X)>=6:
    print('LEAF',len(leaves),'extras',len(X),'time',time.time()-start,flush=True)
    if len(X)>300:continue
    vs=veronese(m,5);B=reduction_basis(S,vs);P=[p for p,c in X];R=[red(vs[p],B) for p in P];th={};relations=[]
    for aa in itertools.combinations(range(len(P)),3):
     z=R[aa[0]][0]^R[aa[1]][0]^R[aa[2]][0]
     for bb in th.get(z,[]):
      if set(aa).isdisjoint(bb):relations.append(aa+bb);break
     if relations:break
     th.setdefault(z,[]).append(aa)
    for rel in relations:
     pp=[P[i] for i in rel];c=0
     for i in rel:c^=R[i][1]
     H=pp+[p for j,p in enumerate(S) if c>>j&1];G=sorted(set(H)^set(p|8192 for p in H)^set(p|8192 for p in S));assert len(G)==300
     C,rk=closure(set(G),veronese(14,5));ans={'seed':seedid,'a':res['a'],'T288':S,'P6':pp,'support300':G,'K5_300':300-rk,'cl5extra300':len(C)};hits.append(ans);print('300BUILT',ans['K5_300'],len(C),flush=True)
     if C:ans['closure_witness']=[C[0][0],C[0][1]]
     json.dump(hits,open('workspace/agent1_new300_from288.json','w'))
     if C:raise SystemExit('NEW302WITNESS')
print('DONE leaves',len(leaves),'hist',dict(hist),'time',time.time()-start)
json.dump({'leaves':leaves,'hist':dict(hist),'hits':hits},open('workspace/agent1_T288_graph13_P6.json','w'));pathlib.Path('workspace/agent1_T288_graph13_P6.py').write_text(pathlib.Path(__file__).read_text())
