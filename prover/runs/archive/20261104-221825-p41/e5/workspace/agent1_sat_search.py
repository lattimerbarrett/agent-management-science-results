from itertools import combinations
import z3, time, json
n=8; q=4
F=[sum(1<<x for x in c) for c in combinations(range(n),q)]
m=len(F)
t=[z3.Int('t%d'%i) for i in range(m)]; h=z3.Int('h')
s=z3.Solver();s.set(timeout=240000)
s.add(z3.Distinct(t));s.add(*[z3.And(x>=1,x<=m) for x in t]);s.add(h>=2,h<m)
s.add(t[0]==1,t[1]==2)
P=[x<=h for x in t]
cover={}
for i,f in enumerate(F):
 for j,g in enumerate(F):
  if i==j:continue
  inter=f&g
  cover[i,j]=[k for k,a in enumerate(F) if k!=i and (a&f).bit_count()==q-1 and inter&a==inter]
# Every non-first present facet has a pure ridge intersection with the earlier prefix.
for i,f in enumerate(F):
 for j,g in enumerate(F):
  if i==j:continue
  s.add(z3.Implies(z3.And(P[i],t[j]<t[i]),z3.Or(*[t[k]<t[i] for k in cover[i,j]])))
# Every omitted facet is blocked by some existing intersection.
for i,f in enumerate(F):
 s.add(z3.Implies(z3.Not(P[i]),z3.Or(*[
  z3.And(P[j],*[z3.Not(P[k]) for k in cover[i,j]])
  for j in range(m) if j!=i
 ])))
# All ambient vertices have appeared.
for v in range(n):s.add(z3.Or(*[P[i] for i,f in enumerate(F) if f>>v&1]))
print('encoded',n,m,'assertions',len(s.assertions()),flush=True)
start=time.time();r=s.check();print('result',r,'time',time.time()-start,flush=True)
if r==z3.sat:
 model=s.model(); hh=model.eval(h).as_long()
 ranks=[model.eval(x).as_long() for x in t]
 order=sorted(range(m),key=lambda i:ranks[i]); prefix=order[:hh]
 def legal(old,i):
  ints=[F[i]&F[j] for j in old];rr=[x for x in ints if x.bit_count()==q-1]
  return not old or bool(rr) and all(any(x&r==x for r in rr) for x in ints)
 old=[]
 for i in prefix:assert legal(old,i);old.append(i)
 assert all(not legal(prefix,i) for i in order[hh:])
 result={'n':n,'d':q-1,'prefix':[[v for v in range(n) if F[i]>>v&1] for i in prefix]}
 print(result)
 with open('workspace/agent1_obstruction.json','w') as out:json.dump(result,out)
else:print(s.reason_unknown())
with open('workspace/agent1_sat_search.py','w') as out:out.write(open(__file__).read())
