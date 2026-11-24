import z3,time,random,json
from itertools import combinations
random.seed(47)
t=6; M=6; a=2;n=t*M
cores=[sum(1<<(M*i+j) for j in range(M)) for i in range(t)]
E=[];roots=[]
for i,C in enumerate(cores):
 for p,q in combinations([v for v in range(n) if not C>>v&1],2):
  roots.append(i);E.append(C|(1<<p)|(1<<q))
x=[z3.Bool('e%d'%i) for i in range(len(E))]
s=z3.Tactic('sat').solver();s.set(timeout=600000)
for i in range(t):s.add(z3.Or([v for v,j in zip(x,roots) if i==j]))
start=time.time()
for p,F in enumerate(E):
 clauses=[]
 for q in range(p):
  if not F&E[q]:clauses.append(z3.Or(z3.Not(x[p]),z3.Not(x[q])))
 s.add(clauses)
print('built',len(E),time.time()-start,flush=True)
fixed=cores[0]|(1<<M)|(1<<(2*M))
s.add(x[E.index(fixed)])
for it in range(10000):
 r=s.check()
 if r!=z3.sat:
  print('candidate solver',r,it,time.time()-start,flush=True);break
 model=s.model();picked=[p for p,v in enumerate(x) if z3.is_true(model.eval(v))]
 # complete the clique greedily to get stronger cover-separation examples
 order=list(range(len(E)));random.shuffle(order)
 for p in order:
  if p not in picked and all(E[p]&E[q] for q in picked):picked.append(p)
 v=[z3.Bool('v%d'%i) for i in range(n)]
 c=z3.SolverFor('QF_FD');c.add(z3.PbEq([(w,1) for w in v],t-1))
 for p in picked:c.add(z3.Or([v[j] for j in range(n) if E[p]>>j&1]))
 count=0
 while count<100 and c.check()==z3.sat:
  cm=c.model();C=sum(1<<j for j,w in enumerate(v) if z3.is_true(cm.eval(w)))
  s.add(z3.Or([x[p] for p,F in enumerate(E) if not F&C]))
  c.add(z3.Or([z3.Not(v[j]) for j in range(n) if C>>j&1]))
  count+=1
 if count==0:
  out=[(roots[p],[j for j in range(n) if (E[p]&~cores[roots[p]])>>j&1]) for p in picked]
  json.dump({'t':t,'M':M,'edges':out},open('construction.json','w'))
  print('FOUND',out,flush=True);break
 if it%10==0:print('iteration',it,'clique',len(picked),'covers',count,'sec',time.time()-start,flush=True)
 if time.time()-start>1200:break
