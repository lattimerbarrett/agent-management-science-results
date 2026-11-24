import z3,itertools
k=5;n=14
patterns=[]
for p in itertools.product([-1,0,1],repeat=k):
 fix=[x for x in p if x!=-1]
 if fix and fix[0]==1:continue
 patterns.append(p)
s=z3.Solver();s.set(timeout=550000)
a=[z3.Int('a%d'%j) for j in range(len(patterns))]
s.add(*[z3.And(x>=0,x<=n) for x in a],sum(a)==n)
for i in range(k):s.add(sum(a[t] for t,p in enumerate(patterns) if p[i]==-1)==7)
def pow2(x):return sum(z3.If(x==i,1<<i,0) for i in range(8))
expr=0
for mask in range(1,1<<k):
 inds=[i for i in range(k) if mask>>i&1]
 d=sum(a[t] for t,p in enumerate(patterns) if all(p[i]==-1 for i in inds))
 bad=[a[t] for t,p in enumerate(patterns) if 0 in [p[i] for i in inds] and 1 in [p[i] for i in inds]]
 valid=sum(bad)==0
 expr+=(-2)**(len(inds)-1)*z3.If(valid,pow2(d),0)
s.add(z3.Or(expr==280,expr==300))
ck=s.check();print(ck,flush=True)
if ck==z3.sat:
 model=s.model();print(model.eval(expr),[(p,model.eval(a[t])) for t,p in enumerate(patterns) if model.eval(a[t]).as_long()],flush=True)
