import json,itertools,time
from z3 import *
x=json.load(open('workspace/agent1_four_subspace_blockprofiles.json'));B=x['blocks'];subs=x['subsets'];flags=json.load(open('workspace/agent1_four_subspace_allflags.json'))
s=Solver();s.set(timeout=240000)
c=[Int('c'+str(i)) for i in range(len(B))]
for i,b in enumerate(B):s.add(c[i]>=0,c[i]<=13//b['D'])
N=Int('N');s.add(Or(N==12,N==13),Sum([c[i]*b['D'] for i,b in enumerate(B)])==N)
for j in range(4):s.add(Sum([c[i]*b['dims'][j] for i,b in enumerate(B)])==7)
d=[Int('d'+str(S)) for S in subs]
for j,S in enumerate(subs):s.add(d[j]==Sum([c[i]*b['intersection_dims'][j] for i,b in enumerate(B)]),d[j]>=0,d[j]<=7)
E=[Sum([If(v==k,1<<k,0) for k in range(8)]) for v in d]
F=Int('F');s.add(Or([F==f for f in flags]))
for f in flags:
 terms=[]
 for j,S in enumerate(subs):
  if f>>j&1:
   if S.bit_count()==2:terms.append(-2*E[j]);s.add(Implies(F==f,d[j]<=5))
   elif S.bit_count()==3:terms.append(4*E[j])
   else:terms.append(-8*E[j])
 s.add(Implies(F==f,512+Sum(terms)<320))
 # Necessary local affine compatibility: each used block has some flag containing global flag.
 for i,b in enumerate(B):
  if not any((g&f)==f for g in b['affine_flags']):s.add(Implies(F==f,c[i]==0))
t=time.time();ans=s.check();print(ans,'time',time.time()-t,flush=True)
if ans==sat:
 m=s.model();out={'N':m[N].as_long(),'F':m[F].as_long(),'dims':[m[v].as_long() for v in d],'blocks':[(i,m[v].as_long()) for i,v in enumerate(c) if m[v].as_long()]};print(out);open('workspace/agent1_four_subspace_relaxation_result.json','w').write(json.dumps(out))
else:open('workspace/agent1_four_subspace_relaxation_result.json','w').write(json.dumps({'status':str(ans)}))
open('workspace/agent1_four_subspace_relaxation.py','w').write(open(__file__).read())
