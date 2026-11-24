import itertools,z3,time,sys,json
sys.path.insert(0,'workspace')
from agent4_checker import dec
n=9;vs=range(n)
tri=[sum(1<<v for v in c) for c in itertools.combinations(vs,3)]
tet=[sum(1<<v for v in c) for c in itertools.combinations(vs,4)]
T={a:z3.Bool('t%d'%a) for a in tri};Q={a:z3.Bool('q%d'%a) for a in tet}
s=z3.Solver();s.set(timeout=60000)
for a in tet:
 ts=[T[b] for b in tri if a&b==b]
 s.add(Q[a]==z3.And(ts));s.add(z3.Sum([z3.If(x,1,0) for x in ts])!=3)
for b in tri:s.add(z3.Implies(T[b],z3.Or([Q[a] for a in tet if a&b==b])))
for e in itertools.combinations(vs,2):
 mask=sum(1<<v for v in e);s.add(z3.Or([Q[a] for a in tet if a&mask==mask]))
f2=z3.Sum([z3.If(x,1,0) for x in T.values()]);f3=z3.Sum([z3.If(x,1,0) for x in Q.values()])
s.add(f2>=(n-2)**2,f3>=f2-n*(n-1)//2+n-1)
s.add(z3.Or([z3.Not(x) for x in T.values()]))
# canonical one missing triangle by symmetry
s.add(z3.Not(T[7]))
# a nonzero H1 cocycle may be represented by chord labels (all edges from0 gauged0).
edges=[(i,j) for i in range(1,n) for j in range(i+1,n)]
def row(t):
 return sum(1<<i for i,e in enumerate(edges) if t&(1<<e[0]) and t&(1<<e[1]))
rows={t:row(t) for t in tri}
def nullvector(mat,width):
 piv={}
 for rr in mat:
  x=rr
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 if len(piv)==width:return None
 f=next(i for i in range(width) if i not in piv);v=1<<f
 for p in sorted(piv):
  if (piv[p]&v).bit_count()%2:v|=1<<p
 assert all((rr&v).bit_count()%2==0 for rr in mat)
 return v
start=time.time();cnt=0;cuts=0
while time.time()-start<300:
 status=s.check()
 if status!=z3.sat:print('RESULT',status,'candidates',cnt,'cuts',cuts,'sec',time.time()-start,flush=True);break
 m=s.model();tr=[a for a in tri if z3.is_true(m.eval(T[a]))];fa=[a for a in tet if z3.is_true(m.eval(Q[a]))]
 nv=nullvector([rows[a] for a in tr],len(edges))
 if nv is not None:
  kill=[T[a] for a in tri if (rows[a]&nv).bit_count()%2]
  s.add(z3.Or(kill));cuts+=1;continue
 cnt+=1
 print('H1zero candidate',cnt,'f',len(tr),len(fa),'cuts',cuts,'sec',time.time()-start,flush=True)
 if dec(tuple(fa),3):
  print('FOUND',fa,flush=True);json.dump({'n':n,'d':3,'facets':fa},open('workspace/agent3_triangle_obstruction.json','w'));break
 s.add(z3.Or([T[a]!=m.eval(T[a]) for a in tri]))
else:print('TIME',cnt,cuts,flush=True)
with open('scratchpad.py') as src,open('workspace/agent3_triangle_sat.py','w') as dst:dst.write(src.read())
