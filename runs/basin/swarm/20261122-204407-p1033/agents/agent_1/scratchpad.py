import z3,itertools,time,json

t=6;k=7;r=2;s=k-r;n=t*s
cores=[sum(1<<v for v in range(i*s,(i+1)*s)) for i in range(t)]
fixed=cores[0]|(1<<s)|(1<<(2*s))
E=[]
for i in range(t):
 out=[v for v in range(n) if not (cores[i]>>v&1)]
 E += [cores[i]|sum(1<<v for v in R) for R in itertools.combinations(out,r)]
E=[a for a in E if a&fixed]
x=[z3.Bool('x%d'%i) for i in range(len(E))]
sol=z3.SolverFor('QF_FD');sol.set(timeout=600000)
sol.add(x[E.index(fixed)])
dis=[[] for a in E]
for i,a in enumerate(E):
 for j in range(i):
  if not a&E[j]:
   sol.add(z3.Or(z3.Not(x[i]),z3.Not(x[j])))
   dis[i].append(j);dis[j].append(i)
for i in range(len(E)):
 sol.add(z3.Or([x[i]]+[x[j] for j in dis[i]]))
for C in itertools.combinations(range(n),t-1):
 c=sum(1<<v for v in C)
 if c&fixed:
  sol.add(z3.Or([x[i] for i,a in enumerate(E) if not a&c]))
print('ready',len(E),flush=True)
a=sol.check();print(a,flush=True)
if a==z3.sat:
 chosen=[a for i,a in enumerate(E) if z3.is_true(sol.model()[x[i]])]
 json.dump(chosen,open('example6k7.json','w'))
 print([[v for v in range(n) if a>>v&1] for a in chosen])
