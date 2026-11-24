import z3,pickle,itertools,random,time
k=6;fs=pickle.load(open('families6.pkl','rb'));mins=[]
for F in fs:
 sets=[a for a in range(1,1<<k) if F>>a&1];mins.append([a for a in sets if not any(b!=a and b&a==b for b in sets)])
for n in [20,40,60,100,150]:
 for seed in range(3):
  vs=random.Random(seed).sample(range(len(fs)),n)
  s=z3.Solver();s.set(timeout=20000)
  x=[[z3.Int(f'x{i}_{v}') for v in range(n)] for i in range(k)]
  for row in x:
   s.add(z3.Distinct(row))
   for a in row:s.add(a>=0,a<n)
  for v in range(n):
   for w in range(n):
    if w==v:continue
    for A in mins[vs[v]]:s.add(z3.Or([x[i][v]>x[i][w] for i in range(k) if A>>i&1]))
  start=time.time();res=s.check();print(n,seed,res,time.time()-start,flush=True)
  if res==z3.unsat:
   pickle.dump(vs,open('unsatfamilies6.pkl','wb'));raise SystemExit
