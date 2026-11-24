import sys
path='workspace/agent3_exact_pointed.py'
s=open(path).read().replace("s.replace('range(1,11)','range(1,D+1)')", "s.replace('range(1,11)','range(1,16)')")
open(path,'w').write(s)
sys.path.insert(0,'workspace')
from agent3_exact_pointed import *
parts=S48['parts'];checked=0
for r in range(8,14):
 for a in range(2):
  for b in range(2):
   for size in range(3*r-24-a-b+1):
    if (23+size+a+b-r)%2:continue
    for sig in parts(size):
     if any(x%3==2 for x in sig):continue
     # P|D - KQ equals sum of valid one-point smooth FZ relations.
     lhs=defaultdict(Fraction)
     for mu,c in core(48,sig).items():
      if sum(mu)==r:lhs[(mu,0)]+=(-1)**(a+b)*c
     for (mu,k),c in tail(r,sig,a,b).items():lhs[(mu,k+1)]-=c
     rhs=defaultdict(Fraction);n1=sig.count(1)
     for m in range(n1+1):
      rem=list(sig)
      for _ in range(m):rem.remove(1)
      cc=(a+b+m)%2
      assert (23+sum(rem)+cc-r)%2==0
      assert 3*r>23+sum(rem)+cc
      fac=(-1)**(a+b+cc)*comb(n1,m)*factorial(m)
      for (mu,(k,)),c in smooth(r,tuple(rem),(cc,)).items():rhs[(mu,k)]+=fac*c
     lhs={m:c for m,c in lhs.items() if c};rhs={m:c for m,c in rhs.items() if c}
     assert lhs==rhs,(r,a,b,sig)
     checked+=1
print('Exact tail restriction checks passed for',checked,'eligible smooth pointed FZ labels')
