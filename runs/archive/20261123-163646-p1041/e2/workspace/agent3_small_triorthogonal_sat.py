import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def parity(v,L):
 shift=1
 while shift<L:v=v^z3.LShR(v,shift);shift*=2
 return z3.Extract(0,0,v)
def solve(n,d,ortho,tm=90000):
 L=n-d-1;cs=[z3.BitVec(f'c{n}_{j}',d) for j in range(L)]
 s=z3.Then('simplify','solve-eqs','bit-blast',z3.With('sat',anf=True,**{'anf.exlin':True,'anf.delay':0})).solver();s.set(timeout=tm)
 for c in cs:s.add(c!=0,*[c!=1<<j for j in range(d)])
 for c,e in zip(cs,cs[1:]):s.add(z3.ULT(c,e))
 rows=[z3.Concat(*[z3.Extract(i,i,c) for c in reversed(cs)]) for i in range(d)]
 for k in range(1,ortho+1):
  for inds in itertools.combinations(range(d),k):
   v=rows[inds[0]]
   for i in inds[1:]:v=v&rows[i]
   s.add(parity(v,L)==(1 if k==1 else 0))
 print('built',n,d,ortho,len(s.assertions()),flush=True);t=time.time();r=s.check();print('res',r,'sec',time.time()-t,flush=True)
 out={'n':n,'d':d,'ortho':ortho,'result':str(r)}
 if r==z3.sat:
  model=s.model();S=[0]+[1<<j for j in range(d)]+[model[c].as_long() for c in cs]
  assert len(set(S))==n
  arr=np.zeros(1<<d,dtype=np.uint8);arr[S]=1;assert degree(arr)<=d-ortho-1
  out['support']=S
 return out
out=[]
for n in [36,38]:
 out.append(solve(n,12,3));pathlib.Path('workspace/agent3_small_triorthogonal_sat.json').write_text(json.dumps(out))
pathlib.Path('workspace/agent3_small_triorthogonal_sat.py').write_text(pathlib.Path(__file__).read_text())
