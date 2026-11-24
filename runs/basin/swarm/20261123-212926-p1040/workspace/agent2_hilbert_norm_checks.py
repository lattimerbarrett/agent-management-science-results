from itertools import product
from pathlib import Path
# The script is also persisted below by an explicit source copy in next step.
class Ring:
 def __init__(self,p,N):self.p=p;self.N=N;self.elts=[self.fromdigits(d) for d in product(range(p),repeat=N)];self.zero=(0,0);self.one=(1,0)
 def fromdigits(self,d):
  a=b=0
  for x in d[::-1]:a,b=-self.p*b,a-self.p*b;a+=x
  return (a,b)
 def norm(self,a,b):
  ds=[]
  for k in range(self.N):
   r=a%self.p;ds.append(r);a-=r;a,b=b-a,-a//self.p
  return self.fromdigits(ds)
 def add(self,x,y):return self.norm(x[0]+y[0],x[1]+y[1])
 def neg(self,x):return self.norm(-x[0],-x[1])
 def mul(self,x,y):
  a,b=x;c,d=y;return self.norm(a*c-self.p*b*d,a*d+b*c-self.p*b*d)
 def scale(self,x,n):return self.norm(n*x[0],n*x[1])
 def power(self,x,n):
  r=self.one
  for k in range(n):r=self.mul(r,x)
  return r
for p,N in [(3,3),(2,4)]:
 R=Ring(p,N);pi=R.norm(0,1);zeta=R.add(R.one,pi);norms=set()
 if p==3:
  for a,b,c in product(R.elts,repeat=3):
   nr=R.add(R.add(R.power(a,3),R.mul(zeta,R.power(b,3))),R.mul(R.power(zeta,2),R.power(c,3)))
   nr=R.add(nr,R.neg(R.scale(R.mul(zeta,R.mul(a,R.mul(b,c))),3)))
   norms.add(nr)
 else:
  for a,b in product(R.elts,repeat=2):norms.add(R.add(R.power(a,2),R.neg(R.mul(zeta,R.power(b,2)))))
 target=R.add(R.one,R.power(pi,N-1))
 print(p,N,'ring',len(R.elts),'normcount',len(norms),'target',target,'innorms?',target in norms)
 assert target not in norms
