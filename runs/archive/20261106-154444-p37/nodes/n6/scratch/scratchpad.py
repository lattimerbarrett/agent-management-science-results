import itertools,z3,random,time,pickle

def product_test(Ple,n,t,timeout=10000):
 m=len(Ple);Q=[frozenset([i]) for i in range(n)]+[frozenset(e) for e in itertools.combinations(range(n),2)];X=list(itertools.product(range(m),Q));N=len(X)
 le=lambda a,b:Ple[a[0]][b[0]] and a[1]<=b[1]
 D=[{j for j in range(N) if j!=i and le(X[j],X[i])} for i in range(N)];U=[{j for j in range(N) if j!=i and le(X[i],X[j])} for i in range(N)]
 crit=[(i,j) for i in range(N) for j in range(N) if i!=j and not le(X[i],X[j]) and not le(X[j],X[i]) and D[i]<=D[j] and U[j]<=U[i]]
 s=z3.Solver();s.set(timeout=timeout);a=[[z3.Int(f'a{k}_{i}') for i in range(N)] for k in range(t)]
 for k in range(t):
  for i in range(N):
   s.add(a[k][i]>=0,a[k][i]<N)
   for j in U[i]:s.add(a[k][i]<a[k][j])
 for i,j in crit:s.add(z3.Or([a[k][i]>a[k][j] for k in range(t)]))
 return s.check(),len(crit)
for seed in range(10):
 rng=random.Random(seed);m=16;perms=[rng.sample(range(m),m) for _ in range(3)];ranks=[{v:i for i,v in enumerate(p)} for p in perms]
 Ple=[[all(r[i]<=r[j] for r in ranks) for j in range(m)] for i in range(m)]
 res,c=product_test(Ple,3,4)
 print(seed,res,'critical pairs',c,flush=True)
 if res==z3.unsat:
  pickle.dump(Ple,open('factor3.pkl','wb'));break
