import json,time,z3,itertools
F=json.load(open('workspace/a4_terminal_CM_1.json'));m=len(F);n=max(F).bit_length()
def subfaces(f):
 x=f
 while x:
  yield x;x=(x-1)&f
 yield 0
faces=set().union(*(set(subfaces(f)) for f in F))
missing=[sum(1<<x for x in c) for c in itertools.combinations(range(n),4) if sum(1<<x for x in c) not in faces]
for f in missing:
 r=sum(1<<v for v in range(n) if f>>v&1 and (f^(1<<v)) in faces)
 assert r in faces,('NOT TERMINAL',f,r)
print('terminal verified',n,m,len(missing),flush=True)
def gf2rank(cols):
 basis={}
 for x in cols:
  while x:
   p=x.bit_length()-1
   if p in basis:x^=basis[p]
   else:basis[p]=x;break
 return len(basis)
def homology(linkfacets):
 ff=set().union(*(set(subfaces(f)) for f in linkfacets))
 dim=max(f.bit_count() for f in ff)-1
 chains={i:sorted(f for f in ff if f.bit_count()==i+1) for i in range(-1,dim+1)}
 ranks={0:1 if chains.get(0) else 0}
 for i in range(1,dim+1):
  ix={f:j for j,f in enumerate(chains[i-1])};cols=[]
  for f in chains[i]:
   cols.append(sum(1<<ix[f^(1<<v)] for v in range(n) if f>>v&1))
  ranks[i]=gf2rank(cols)
 ranks[dim+1]=0
 return dim,[len(chains[i])-ranks[i]-ranks[i+1] for i in range(dim+1)]
for tau in faces:
 lf=[f^tau for f in F if f&tau==tau]
 dim,betti=homology(lf)
 assert all(x==0 for x in betti[:dim]),('NONCM',tau,dim,betti)
print('all links CM overGF2 verified',len(faces),flush=True)

# Exact shellability encoding. Non-first facets choose their restriction faces.
s=z3.Solver();s.set(timeout=240000)
t=[z3.Int('t%d'%i) for i in range(m)];s.add(z3.Distinct(t));s.add(*[z3.And(x>=1,x<=m) for x in t])
R={}
for i,f in enumerate(F):
 vs=[v for v in range(n) if f>>v&1]
 for v in vs:
  r=R[i,v]=z3.Bool('r%d_%d'%(i,v));ridge=f^(1<<v)
  nn=[j for j,g in enumerate(F) if j!=i and g&ridge==ridge]
  s.add(z3.Implies(r,z3.Or(*[t[j]<t[i] for j in nn])))
 s.add(z3.Implies(t[i]>1,z3.Or(*[R[i,v] for v in vs])))
 for j,g in enumerate(F):
  if i!=j:
   s.add(z3.Implies(t[j]<t[i],z3.Or(*[R[i,v] for v in vs if not(g>>v&1)])))
print('encoded shellability',len(s.assertions()),flush=True)
start=time.time();res=s.check();print('result',res,'time',time.time()-start,flush=True)
if res==z3.sat:
 model=s.model();order=sorted(range(m),key=lambda i:model.eval(t[i]).as_long())
 old=set();out=[]
 for i in order:
  f=F[i];restriction=sum(1<<v for v in range(n) if f>>v&1 and f^(1<<v) in old)
  if old:assert restriction not in old
  old.update(subfaces(f));out.append(f)
 print('SHELLING CERTIFIED',flush=True)
 with open('workspace/agent1_terminal_shelling.json','w') as ff:json.dump(out,ff)
else:print(s.reason_unknown())
with open('workspace/agent1_n16_candidate_shellability.py','w') as ff:ff.write(open(__file__).read())
