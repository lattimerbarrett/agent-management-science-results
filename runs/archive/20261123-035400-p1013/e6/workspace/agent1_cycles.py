"""Exact cycle counts of joins. All arithmetic is integral or rational.
The component polynomial Q counts unoriented path forests with orientations
on every nonsingleton path. Suitable for tiny internal graphs or disjoint
unions of repeatedly used fixed components.
"""
from math import factorial, comb
from fractions import Fraction
from itertools import combinations

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]+=x*y
 return c

def power(a,n):
 out=[1]
 while n:
  if n&1: out=mul(out,a)
  a=mul(a,a);n//=2
 return out

def path_polynomial(n,edges):
 # Exhaustive verified directly for graphs with few internal edges.
 ans=[comb(n,k) for k in range(n+1)]
 for mask in range(1,1<<len(edges)):
  deg=[0]*n; parent=list(range(n)); selected=set();ok=True
  def find(x):
   while parent[x]!=x:
    x=parent[x]
   return x
  for i,(u,v) in enumerate(edges):
   if not (mask>>i)&1:continue
   deg[u]+=1;deg[v]+=1
   if deg[u]>2 or deg[v]>2 or find(u)==find(v):ok=False;break
   parent[find(u)]=find(v);selected.update((u,v))
  if not ok:continue
  components=len(selected)-mask.bit_count()
  for isolated in range(n-len(selected)+1):
   ans[components+isolated]+=(1<<components)*comb(n-len(selected),isolated)
 return ans

def _weights(q):return [factorial(k)*v for k,v in enumerate(q)]

def cycles_join_r2(q1,q2,n1,n2,internal_cycles=0):
 w1,w2=_weights(q1),_weights(q2)
 s=sum(Fraction(w1[k]*w2[k],k) for k in range(1,min(len(w1),len(w2))))
 ans=(s-n1*n2)/2+internal_cycles
 assert ans.denominator==1
 return int(ans)

def cycles_join_r3(q1,q2,q3,sizes,internal_cycles=0):
 # -log(1-xy-xz-yz-2xyz), multinomial expansion.
 w1,w2,w3=map(_weights,(q1,q2,q3));n1,n2,n3=sizes
 fac=[factorial(i) for i in range(n1+n2+n3+1)]
 total=Fraction(0)
 for d in range(min(n1,n2,n3)+1):
  for a in range(min(n1-d,n2-d)+1):
   for b in range(min(n1-a-d,n3-d)+1):
    for c in range(min(n2-a-d,n3-b-d)+1):
     k=a+b+c+d
     if not k: continue
     i,j,l=a+b+d,a+c+d,b+c+d
     num=fac[k-1]*(1<<d)*w1[i]*w2[j]*w3[l]
     den=fac[a]*fac[b]*fac[c]*fac[d]
     total+=Fraction(num,den)
 ans=(total-n1*n2-n1*n3-n2*n3)/2+internal_cycles
 assert ans.denominator==1
 return int(ans)

def brute_cycles(n,edges):
 adj=[set() for _ in range(n)]
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 count=0
 for start in range(n):
  def walk(path,used):
   nonlocal count
   for v in adj[path[-1]]:
    if v==start:
     if len(path)>=3:count+=1
    elif v>start and not ((used>>v)&1):walk(path+[v],used|(1<<v))
  walk([start],1<<start)
 return count//2

def check():
 assert path_polynomial(2,[(0,1)])==[1,4,1]
 assert path_polynomial(3,[(0,1),(1,2),(0,2)])==[1,15,9,1]
 # Exhaustively test every graph on <=4 vertices as first joined class,
 # and <=2 isolated vertices in each of 1 or 2 other classes.
 checked=0
 for n in range(1,5):
  poss=list(combinations(range(n),2))
  for mask in range(1<<len(poss)):
   es=[e for i,e in enumerate(poss) if mask>>i&1]
   q=path_polynomial(n,es);internal=brute_cycles(n,es)
   for m in range(1,3):
    edges=es+[(i,n+j) for i in range(n) for j in range(m)]
    got=cycles_join_r2(q,power([1,1],m),n,m,internal)
    assert got==brute_cycles(n+m,edges),(n,m,es,got)
    checked+=1
    for l in range(1,3):
     edges3=edges+[(i,n+m+j) for i in range(n+m) for j in range(l)]
     got=cycles_join_r3(q,power([1,1],m),power([1,1],l),(n,m,l),internal)
     assert got==brute_cycles(n+m+l,edges3),(n,m,l,es,got)
     checked+=1
 return checked
if __name__=='__main__':print('exact cycle join checks:',check())
