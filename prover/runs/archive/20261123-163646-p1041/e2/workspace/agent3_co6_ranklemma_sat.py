import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def parity(v,L):
 shift=1
 while shift<L:
  v=v^z3.LShR(v,shift);shift*=2
 return z3.Extract(0,0,v)

def solve(n,timeout=55000):
 L=n-15;cs=[z3.BitVec(f'c{n}_{j}',14) for j in range(L)]
 sat=z3.With('sat',anf=True,**{'anf.exlin':True,'anf.delay':0})
 s=z3.Then('simplify','solve-eqs','bit-blast',sat).solver();s.set(timeout=timeout)
 for c in cs:s.add(c!=0,*[c!=1<<j for j in range(14)])
 for c,d in zip(cs,cs[1:]):s.add(z3.ULT(c,d))
 rows=[z3.Concat(*[z3.Extract(i,i,c) for c in reversed(cs)]) for i in range(14)]
 for k in range(1,6):
  for inds in itertools.combinations(range(14),k):
   v=rows[inds[0]]
   for i in inds[1:]:v=v&rows[i]
   s.add(parity(v,L)==(1 if k==1 else 0))
 print('built',n,'constraints',len(s.assertions()),flush=True);t=time.time();result=s.check();print('result',n,result,'sec',time.time()-t,flush=True)
 out={'n':n,'result':str(result)}
 if result==z3.sat:
  model=s.model();S=[0]+[1<<j for j in range(14)]+[model[c].as_long() for c in cs]
  assert len(S)==len(set(S))==n
  arr=np.zeros(1<<14,dtype=np.uint8);arr[S]=1;assert degree(arr)<=8
  out['support']=S
 return out
out=[]
for n in [156,154,152]:
 out.append(solve(n));pathlib.Path('workspace/agent3_co6_ranklemma_sat.json').write_text(json.dumps(out))
pathlib.Path('workspace/agent3_co6_ranklemma_sat.py').write_text(pathlib.Path(__file__).read_text())
