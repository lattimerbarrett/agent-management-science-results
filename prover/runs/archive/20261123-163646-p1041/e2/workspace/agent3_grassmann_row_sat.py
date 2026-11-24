import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def par(v,L=128):
 for shift in [64,32,16,8,4,2,1]:v=v^z3.LShR(v,shift)
 return z3.Extract(0,0,v)
start=time.time();U=[z3.BitVec(f'u{x}',8) for x in range(128)];V=[z3.BitVec(f'v{x}',8) for x in range(128)]
s=z3.Then('simplify','solve-eqs','bit-blast',z3.With('sat',anf=True,**{'anf.exlin':True,'anf.delay':0})).solver();s.set(timeout=30000)
for u,v in zip(U,V):s.add(z3.Or(z3.And(u==0,v==0),z3.And(z3.ULT(0,u),z3.ULT(u,v),z3.ULT(v,u^v))))
s.add(U[0]==1,V[0]==2)
ct=z3.Sum([z3.If(u!=0,1,0) for u in U]);s.add(z3.Or(*[ct==a for a in [97,99,101,103]]))
u=[z3.Concat(*[z3.Extract(j,j,a) for a in reversed(U)]) for j in range(8)]
v=[z3.Concat(*[z3.Extract(j,j,a) for a in reversed(V)]) for j in range(8)]
w=[a^b for a,b in zip(u,v)]
inputmasks={}
for d in range(5):
 inputmasks[d]=[]
 for k in range(d+1):
  for T in itertools.combinations(range(7),k):
   mask=sum(1<<i for i in T);val=sum(1<<x for x in range(128) if x&mask==mask);inputmasks[d].append(z3.BitVecVal(val,128))
for j in range(2,7):
 for J in itertools.combinations(range(8),j):
  aa=u[J[0]];bb=v[J[0]];cc=w[J[0]]
  for i in J[1:]:aa=aa&u[i];bb=bb&v[i];cc=cc&w[i]
  mom=aa^bb^cc
  for mask in inputmasks[6-j]:s.add(par(mom&mask)==0)
print('built',len(s.assertions()),'sec',time.time()-start,flush=True);t=time.time();result=s.check();print('result',result,'sec',time.time()-t,flush=True)
out={'result':str(result)}
if result==z3.sat:
 model=s.model();us=[model[a].as_long() for a in U];vv=[model[a].as_long() for a in V]
 arr=np.zeros(1<<15,dtype=np.uint8)
 for x,(a,b) in enumerate(zip(us,vv)):
  for y in [a,b,a^b]:arr[x+(y<<7)]^=1
 assert int(arr.sum()) in [322,326,330,334]
 assert degree(arr)<=8
 out.update({'weight':int(arr.sum()),'U':us,'V':vv,'support':np.flatnonzero(arr).tolist()})
pathlib.Path('workspace/agent3_grassmann_row_sat.json').write_text(json.dumps(out))
pathlib.Path('workspace/agent3_grassmann_row_sat.py').write_text(pathlib.Path(__file__).read_text())
