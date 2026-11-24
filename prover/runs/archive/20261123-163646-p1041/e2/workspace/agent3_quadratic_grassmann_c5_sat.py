import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def rotmask(x):return (x&~31)|((x&15)<<1)|((x>>4)&1)
def outrot(j):return (j+1)%5 if j<5 else j
def xxor(xs):
 if not xs:return z3.BoolVal(False)
 v=xs[0]
 for x in xs[1:]:v=z3.Xor(v,x)
 return v
def parity(v):
 for shift in [64,32,16,8,4,2,1]:v=v^z3.LShR(v,shift)
 return z3.Extract(0,0,v)
start=time.time()
mons=[sum(1<<i for i in T) for k in range(3) for T in itertools.combinations(range(7),k)]
orbits=[];seen={}
for j in range(8):
 for mask in mons:
  if (j,mask) in seen:continue
  orb=[];p=(j,mask)
  while p not in orb:orb.append(p);p=(outrot(p[0]),rotmask(p[1]))
  idx=len(orbits);orbits.append(orb)
  for p in orb:seen[p]=idx
cu=[z3.Bool(f'cu{i}') for i in range(len(orbits))];cv=[z3.Bool(f'cv{i}') for i in range(len(orbits))]
U=[];V=[]
for x in range(128):
 ub=[];vb=[]
 for j in range(8):
  odd=set()
  for mask in mons:
   if x&mask!=mask:continue
   i=seen[(j,mask)]
   if i in odd:odd.remove(i)
   else:odd.add(i)
  ub.append(xxor([cu[i] for i in odd]));vb.append(xxor([cv[i] for i in odd]))
 U.append(z3.Concat(*[z3.If(a,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for a in reversed(ub)]))
 V.append(z3.Concat(*[z3.If(a,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for a in reversed(vb)]))
reps=[];done=set();fixed=[]
for x in range(128):
 if x in done:continue
 reps.append(x);y=x
 while y not in done:done.add(y);y=rotmask(y)
 if rotmask(x)==x:fixed.append(x)
s=z3.Then('simplify','solve-eqs','bit-blast',z3.With('sat',anf=True,**{'anf.exlin':True,'anf.delay':0})).solver();s.set(timeout=90000)
s.add(U[0]==31,V[0]==32)
pbs=[(z3.And(U[x]!=0,V[x]!=0,U[x]!=V[x]),1 if x in fixed else 5) for x in reps]
s.add(z3.Or(*[z3.PbEq(pbs,a) for a in [97,99,101,103]]))
u=[z3.Concat(*[z3.Extract(j,j,a) for a in reversed(U)]) for j in range(8)]
v=[z3.Concat(*[z3.Extract(j,j,a) for a in reversed(V)]) for j in range(8)]
w=[a^b for a,b in zip(u,v)]
inputmasks={}
for d in range(5):
 inputmasks[d]=[]
 for k in range(d+1):
  for T in itertools.combinations(range(7),k):
   mask=sum(1<<i for i in T);val=sum(1<<x for x in range(128) if x&mask==mask);inputmasks[d].append((mask,z3.BitVecVal(val,128)))
for j in range(2,7):
 for J in itertools.combinations(range(8),j):
  aa=u[J[0]];bb=v[J[0]];cc=w[J[0]]
  for i in J[1:]:aa=aa&u[i];bb=bb&v[i];cc=cc&w[i]
  mom=aa^bb^cc
  for imask,mask in inputmasks[6-j]:
   jmask=sum(1<<i for i in J);orb=[];p=jmask;q=imask
   for rr in range(5):orb.append((p,q));p=rotmask(p);q=rotmask(q)
   if (jmask,imask)!=min(orb):continue
   s.add(parity(mom&mask)==0)
print('coefficients',2*len(orbits),'constraints',len(s.assertions()),'builtsec',time.time()-start,flush=True)
t=time.time();result=s.check();print('result',result,'sec',time.time()-t,flush=True)
out={'result':str(result),'reason':s.reason_unknown() if result==z3.unknown else None}
if result==z3.sat:
 model=s.model();us=[model.eval(a).as_long() for a in U];vv=[model.eval(a).as_long() for a in V]
 arr=np.zeros(1<<15,dtype=np.uint8)
 for x,(a,b) in enumerate(zip(us,vv)):
  for y in [a,b,a^b]:arr[x+(y<<7)]^=1
 assert int(arr.sum()) in [322,326,330,334];assert degree(arr)<=8
 out.update({'weight':int(arr.sum()),'U':us,'V':vv,'support':np.flatnonzero(arr).tolist()})
pathlib.Path('workspace/agent3_quadratic_grassmann_c5_sat.json').write_text(json.dumps(out))
pathlib.Path('workspace/agent3_quadratic_grassmann_c5_sat.py').write_text(pathlib.Path(__file__).read_text())
