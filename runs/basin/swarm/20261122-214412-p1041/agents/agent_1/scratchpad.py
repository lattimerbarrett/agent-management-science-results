import z3,itertools,pickle,time
for n in [7]:
 E=1<<n;s=z3.Solver();s.set(timeout=3600000)
 patterns=[p for p in range(1,E) if (p&3) in [1,2]]
 counts={p:z3.Int('n%d'%p) for p in patterns}
 for x in counts.values():s.add(x>=0,x<=7)
 for i in range(n):s.add(sum(v for p,v in counts.items() if (p>>i)&1)==7)
 ka=[sum(v for p,v in counts.items() if p&1 and (p>>i)&1) for i in range(2,n)]
 for i in range(len(ka)-1):s.add(ka[i]<=ka[i+1])
 s.add(ka[0]<=3)
 for i in range(2,n-1):
  for j in range(i+1,n):
   # Within an equal ka class, sort intersections with earlier rows lexicographically.
   left=[];right=[]
   for h in range(2,i):
    left.append(sum(v for p,v in counts.items() if (p>>i)&1 and (p>>h)&1))
    right.append(sum(v for p,v in counts.items() if (p>>j)&1 and (p>>h)&1))
   if left:
    s.add(z3.Implies(ka[i-2]==ka[j-2],z3.Or([z3.And(*[left[t]==right[t] for t in range(h)],left[h]<=right[h]) for h in range(len(left))])))
 I={}
 for a in range(1,E):
  u=sum(v for p,v in counts.items() if p&a);I[a]=z3.Int('I%d'%a)
  s.add(z3.Or([z3.And(u==k,I[a]==1<<(14-k)) for k in range(7,15)]))
  if a.bit_count()==2:s.add(I[a]!=64,I[a]!=128)
 w=sum(((-2)**(a.bit_count()-1))*I[a] for a in range(1,E))
 print('n',n,'ready',flush=True)
 for target in [322]:
  s.push();s.add(w==target);res=s.check();print(n,target,res,flush=True)
  if res==z3.sat:
   M=s.model();cnt={p:M[v].as_long() for p,v in counts.items()};cols=[p for p,c in cnt.items() for _ in range(c)];mons=[sum(1<<j for j,p in enumerate(cols) if (p>>i)&1) for i in range(n)]
   print('FOUND',mons,flush=True);pickle.dump(mons,open('coord%d.pkl'%target,'wb'))
  s.pop()
