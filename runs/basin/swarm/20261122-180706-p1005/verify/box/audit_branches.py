import final_code as F
import inspect,pickle,time
from collections import Counter
src=inspect.getsource(F.enumerate_nests)
src=src.replace('def enumerate_nests(D):','def enumerate_branch(D, branch=None, frontier=False):')
src=src.replace('        k = len(sol)\n','        k = len(sol)\n        if frontier and k == 3:\n            out.append((sol, U, O, A, G))\n            return\n')
src=src.replace('    rec(\n        [root], M[root], M[root],\n        ((1 << B)-1) ^ (1 << root),\n        initial_group\n    )','    if branch is None:\n        rec([root], M[root], M[root], ((1 << B)-1) ^ (1 << root), initial_group)\n    else:\n        rec(*branch)')
ns=vars(F).copy(); exec(src,ns); enum=ns['enumerate_branch']
D=F.make(11)
f=enum(D,frontier=True)
old=pickle.load(open('agents/agent_1/front11.pkl','rb'))
assert f==old
print('Frontier identical,',len(f),'states',flush=True)
raw=pickle.load(open('agents/agent_1/raw11.pkl','rb')); rawset=set(raw)
prefix=pickle.load(open('agents/agent_1/partial11.pkl','rb'))
combined=list(prefix)
for i in range(453,len(f)):
 combined.extend(pickle.load(open(f'agents/agent_1/jobs11/{i}.pkl','rb')))
assert raw==combined
print('q11 raw is exact prefix + jobs 453..668; prefix',len(prefix),'total',len(raw),flush=True)
for i in [0,452,549,550,668]:
 t=time.time(); out=enum(D,branch=f[i]); F.check_nests(D,out)
 assert set(out)<=rawset
 if i>=453:
  oldout=pickle.load(open(f'agents/agent_1/jobs11/{i}.pkl','rb'))
  assert out==oldout
 bad=[s for s in out if not F.hemi(D,s)]
 print('rerun job',i,'seed',f[i][0],'search',Counter(map(len,out)),'bad',Counter(map(len,bad)),'elapsed',time.time()-t,flush=True)
