import json,time
from z3 import *
x=json.load(open('workspace/agent1_four_subspace_blockprofiles.json'));B=x['blocks'];subs=x['subsets']
s=Solver();s.set(timeout=240000)
c=[];types=[]
for i,b in enumerate(B):
 for f in b['affine_flags']:
  v=Int('c_%d_%d'%(i,f));s.add(v>=0,v<=14//b['D']);c.append(v);types.append((i,f))
a=[Sum([v for v,(i,f) in zip(c,types) if i==j]) for j in range(len(B))]
N=Int('N');s.add(N==14,Sum([a[i]*b['D'] for i,b in enumerate(B)])==N)
for j in range(4):s.add(Sum([a[i]*b['dims'][j] for i,b in enumerate(B)])==7)
d=[Int('d'+str(S)) for S in subs]
for j,S in enumerate(subs):s.add(d[j]==Sum([a[i]*b['intersection_dims'][j] for i,b in enumerate(B)]),d[j]>=0,d[j]<=7)
E=[Sum([If(v==k,1<<k,0) for k in range(8)]) for v in d]
J=[];w=IntVal(512)
for j,S in enumerate(subs):
 z=Bool('J'+str(S));J.append(z);s.add(z==(Sum([v for v,(i,f) in zip(c,types) if not f>>j&1])==0))
 if S.bit_count()==2:w+=If(z,-2*E[j],0);s.add(Implies(z,d[j]<=5))
 elif S.bit_count()==3:w+=If(z,4*E[j],0)
 else:w+=If(z,-8*E[j],0)
s.add(Or(*[w==k for k in (322,326,330,334)]))
t=time.time();ans=s.check();print(ans,'time',time.time()-t,'vars',len(c),flush=True)
out={'status':str(ans),'seconds':time.time()-t}
if ans==sat:
 m=s.model();out.update({'N':m[N].as_long(),'weight':m.eval(w).as_long(),'F':sum((1<<j) for j,z in enumerate(J) if is_true(m[z])),'dims':[m[v].as_long() for v in d],'types':[(i,f,m[v].as_long()) for v,(i,f) in zip(c,types) if m[v].as_long()]});print(out)
open('workspace/agent3_four_subspace_target_result.json','w').write(json.dumps(out))

