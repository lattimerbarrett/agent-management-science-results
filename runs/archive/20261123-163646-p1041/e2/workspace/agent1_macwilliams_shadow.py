"""Necessary weight-enumerator feasibility constraints, not a RM spectrum proof."""
import math,z3,json

def krawtchouk(n,i,j):
 return sum((-1)**h*math.comb(j,h)*math.comb(n-j,i-h)
            for h in range(max(0,i-(n-j)),min(i,j)+1))

def feasibility(n,k,d,timeout=30000):
 # Hypothesis: self-orthogonal binary [n,k,>=d], all-one vector present,
 # distinct generator columns (dual has no weight-two words).
 assert n%4==2
 weights=[0,n]+list(range(d,n-d+1,2))
 A={j:z3.Int(f'A_{n}_{j}') for j in weights}
 s=z3.Solver();s.set(timeout=timeout)
 s.add(A[0]==1,A[n]==1,*[x>=0 for x in A.values()],sum(A.values())==2**k)
 for j in weights:s.add(A[j]==A[n-j])
 # q(c)=wt(c)/2 mod2 is linear on a self-orthogonal code.
 # q(1)=1 since n=2mod4, so C0=ker(q) has dimension k-1.
 s.add(sum(v for j,v in A.items() if j%4==0)==2**(k-1))
 for i in range(n+1):
  Bnum=sum(krawtchouk(n,i,j)*v for j,v in A.items())
  s.add(Bnum>=0,Bnum%(2**k)==0)
  # C subset Cdual.
  s.add(Bnum>=2**k*A.get(i,0))
  # all-ones gives even dual; distinct generator columns prohibit weight2.
  if i%2 or i==2:s.add(Bnum==0)
  # MacWilliams for the doubly-even subcode C0, including shadow positivity.
  Dnum=sum(krawtchouk(n,i,j)*v for j,v in A.items() if j%4==0)
  s.add(Dnum>=0,Dnum%(2**(k-1))==0)
 result=s.check()
 return str(result), ({j:s.model()[v].as_long() for j,v in A.items()} if result==z3.sat else None)

if __name__=='__main__':
 out={}
 for n,k,d in [(322,16,154),(326,16,156),(330,16,158),(334,16,158)]:
  r,model=feasibility(n,k,d)
  print((n,k,d),r)
  assert r=='unsat'
  out[str((n,k,d))]=r
 print('Only conditional code-parameter exclusions; no full RM weight exclusion follows alone.')
