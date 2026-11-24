import itertools, z3, time

def solve(t,rs,ext=0,seconds=60,k=None):
 k=t if k is None else k
 cores=[];n=0
 for r in rs:
  cores.append(set(range(n,n+k-r)));n+=k-r
 n+=ext
 edges=[];groups=[]
 for i,(X,r) in enumerate(zip(cores,rs)):
  for R in itertools.combinations(set(range(n))-X,r):
   edges.append(sum(1<<v for v in X.union(R)));groups.append(i)
 print('n,edges',n,len(edges),flush=True)
 s=z3.Solver();s.set(timeout=seconds*1000)
 vs=[z3.Bool('e'+str(j)) for j in range(len(edges))]
 for a in range(len(edges)):
  for b in range(a):
   if not edges[a]&edges[b]:s.add(z3.Or(z3.Not(vs[a]),z3.Not(vs[b])))
 for C in itertools.combinations(range(n),t-1):
  mask=sum(1<<v for v in C)
  ids=[j for j,e in enumerate(edges) if not e&mask]
  if not ids:return print('impossible cover',C)
  s.add(z3.Or([vs[j] for j in ids]))
 print('built',flush=True);result=s.check();print(result,flush=True)
 if result==z3.sat:
  model=s.model();selected=[(groups[j],[v for v in range(n) if e>>v&1]) for j,e in enumerate(edges) if z3.is_true(model[vs[j]])]
  print('cores',cores,'selected',selected,flush=True)
# The elementary ordered-join composition has
# T(a+b) <= T(a)+T(b)+a*b.  Iterating balanced joins remains quadratic.
T={1:0}
for n in range(2,65):
 a=n//2;b=n-a
 T[n]=T[a]+T[b]+a*b
print([(n,T[n]) for n in [2,4,8,16,32,64]])
# Padding a group of edge size d_i to K adds K-d_i private
# core points, leaving its deficit d_i-|X_i| unchanged.
# Check this numerically on a nonuniform list of groups.
sizes=[7,9,12]; coresizes=[5,8,9]; K=max(sizes)
before=sum(d-x for d,x in zip(sizes,coresizes))
after=sum(K-(x+K-d) for d,x in zip(sizes,coresizes))
print('nonuniform padding:',before,after)

