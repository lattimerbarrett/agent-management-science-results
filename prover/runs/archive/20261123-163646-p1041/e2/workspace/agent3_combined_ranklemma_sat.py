import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree
L=141
cs=[z3.BitVec(f'c{j}',14) for j in range(L)]
act=[c!=0 for c in cs]

def parity(v,L):
 shift=1
 while shift<L:v=v^z3.LShR(v,shift);shift*=2
 return z3.Extract(0,0,v)
start=time.time()
sat=z3.With('sat',max_memory=3500,anf=True,**{'anf.exlin':False,'anf.delay':0})
s=z3.Then('simplify','solve-eqs','bit-blast',sat).solver();s.set(timeout=600000)
for j,c in enumerate(cs):
 s.add(*[c!=1<<i for i in range(14)])
 if j<49:s.add(act[j])
 if j:s.add(z3.Implies(act[j],z3.And(act[j-1],z3.ULT(cs[j-1],c))))
avec=z3.Concat(*[z3.If(a,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for a in reversed(act)])
s.add(parity(avec,L)==1)
rows=[z3.Concat(*[z3.Extract(i,i,c) for c in reversed(cs)]) for i in range(14)]
for k in range(1,6):
 for inds in itertools.combinations(range(14),k):
  v=rows[inds[0]]
  for i in inds[1:]:v=v&rows[i]
  s.add(parity(v,L)==(1 if k==1 else 0))
print('built',len(s.assertions()),'sec',time.time()-start,flush=True)
pathlib.Path('workspace/agent3_combined_ranklemma_sat.py').write_text(pathlib.Path(__file__).read_text())
t=time.time()
try:
 r=s.check();reason=s.reason_unknown() if r==z3.unknown else None
except z3.Z3Exception as e:r='exception';reason=str(e)
print('result',r,'reason',reason,'sec',time.time()-t,flush=True)
out={'result':str(r),'reason':reason,'runtime':time.time()-t}
if r==z3.sat:
 model=s.model();S=[0]+[1<<i for i in range(14)]+[model[c].as_long() for c in cs if model[c].as_long()!=0]
 assert len(S)==len(set(S)) and len(S)<=156
 arr=np.zeros(1<<14,dtype=np.uint8);arr[S]=1;assert degree(arr)<=8
 out['support']=S;out['weight']=len(S)
pathlib.Path('workspace/agent3_combined_ranklemma_sat.json').write_text(json.dumps(out))
