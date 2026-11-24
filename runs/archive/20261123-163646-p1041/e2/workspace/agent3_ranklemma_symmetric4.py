import itertools,math,z3,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def parts(n,k,lo=1):
 if k==0:
  if n==0:yield ()
  return
 for a in range(lo,n//k+1):
  for p in parts(n-a,k-1,a):yield (a,)+p

def subs(n):
 a=n
 while True:
  yield a
  if a==0:break
  a=(a-1)&n

def check(bs,timeout=5000):
 orbs=list(itertools.product(*[range(b+1) for b in bs]));idx={o:i for i,o in enumerate(orbs)};M=len(orbs)
 weights=[math.prod(math.comb(b,i) for b,i in zip(bs,o)) for o in orbs]
 rows=[]
 for J in orbs:
  if sum(J)>8:rows.append((sum(1<<idx[I] for I in itertools.product(*[list(subs(j)) for j in J])),0))
 for i,w in enumerate(weights):
  if w>156:rows.append((1<<i,0))
 for J in [(0,)*len(bs)]+[tuple(int(i==j) for i in range(len(bs))) for j in range(len(bs))]:rows.append((1<<idx[J],1))
 basis={}
 for mask,rhs in rows:
  while mask:
   p=mask.bit_length()-1
   if p not in basis:basis[p]=(mask,rhs);break
   mm,rr=basis[p];mask^=mm;rhs^=rr
  if mask==0 and rhs:return {'blocks':bs,'result':'unsat_linear','free':M-len(basis)}
 free=[j for j in range(M) if j not in basis];expr={j:z3.Bool('f'+str(j)) for j in free}
 def xo(xs):
  v=z3.BoolVal(False)
  for x in xs:v=z3.Xor(v,x)
  return v
 for p in sorted(basis):
  mask,rhs=basis[p];expr[p]=xo([z3.BoolVal(bool(rhs))]+[expr[j] for j in range(p) if mask>>j&1])
 s=z3.Solver();s.set(timeout=timeout)
 pb=[(expr[j],weights[j]) for j in range(M)]
 s.add(z3.Or(*[z3.PbEq(pb,w) for w in [128,136,144,148,152,154,156]]))
 t=time.time();r=s.check();out={'blocks':bs,'result':str(r),'free':len(free),'time':time.time()-t}
 if r==z3.sat:
  model=s.model();vals={o:bool(z3.is_true(model.eval(expr[j],model_completion=True))) for j,o in enumerate(orbs)}
  S=[]
  for x in range(1<<14):
   J=[];shift=0
   for b in bs:J.append(((x>>shift)&((1<<b)-1)).bit_count());shift+=b
   if vals[tuple(J)]:S.append(x)
  arr=np.zeros(1<<14,dtype=np.uint8);arr[S]=1
  assert len(S) in [128,136,144,148,152,154,156] and degree(arr)<=8
  assert all(x in S for x in [0]+[1<<j for j in range(14)])
  out['support']=S
 return out
out=[]
for k in [4]:
 for bs in parts(14,k):
  r=check(bs,2000);print(r['blocks'],r['result'],r['free'],flush=True);out.append(r)
  pathlib.Path('workspace/agent3_ranklemma_symmetric4.json').write_text(json.dumps(out))
  if 'support' in r:raise SystemExit
pathlib.Path('workspace/agent3_ranklemma_symmetric4.py').write_text(pathlib.Path(__file__).read_text())
