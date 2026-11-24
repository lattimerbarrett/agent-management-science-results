import z3,itertools
for pairs in itertools.combinations(range(5),3):
 a=[z3.Real('a%d'%i)for i in range(5)];b=[z3.Real('b%d'%i)for i in range(5)];s=z3.Optimize()
 for x in a+b:s.add(x>=0)
 for i in range(5):
  p=(i-1)%5;n=(i+1)%5
  s.add(z3.Implies(a[i]>0,z3.And(b[n]+a[p]>=1,b[n]+a[n]>=1)))
  s.add(z3.Implies(b[i]>0,z3.And(a[p]+b[p]>=1,a[p]+b[n]>=1)))
 for i in pairs:s.add(a[i]+b[(i+2)%5]>=2)
 q=sum(a+b);s.minimize(q);s.check();md=s.model();print(pairs,md.eval(q),[md.eval(x)for x in a],[md.eval(x)for x in b])
