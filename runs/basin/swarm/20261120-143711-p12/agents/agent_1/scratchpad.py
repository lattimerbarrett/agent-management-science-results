from sage.all import *
from functools import lru_cache
from collections import Counter
N=12; p=1000000007; F=QQ
T=PowerSeriesRing(F,'t',default_prec=N+1); t=T.gen()
A=T([F(factorial(6*n))/F(factorial(3*n)*factorial(2*n)) for n in range(N+1)])
B=T([F(factorial(6*n))*F(6*n+1)/F(factorial(3*n)*factorial(2*n)*(6*n-1)) for n in range(N+1)])
Q=B/A
P=PolynomialRing(F,['k'+str(i) for i in range(1,N+1)]); ks=[P(48)]+list(P.gens())
def trunc(f):
 return P({m:c for m,c in f.dict().items() if sum((i+1)*a for i,a in enumerate(m))<=N})
def mul(a,b): return trunc(a*b)
E=[P(1)]
L=A.log()
for d in range(1,N+1):
 E.append(-sum(F(i)*L[i]*ks[i]*E[d-i] for i in range(1,d+1))/F(d))
@lru_cache(None)
def block(sig):
 shift=sum(x//3 for x in sig); nb=sum(x%3==1 for x in sig)
 S=(t**shift)*Q**nb
 return factorial(len(sig)-1)*sum(S[i]*ks[i] for i in range(N+1))
@lru_cache(None)
def mark(sig):
 if not sig:return P(1)
 a=sig[0]; tail=Counter(sig[1:]); items=list(tail)
 ans=P(0)
 for counts in cartesian_product([range(tail[x]+1) for x in items]):
  sub=tuple(sorted([a]+[x for x,c in zip(items,counts) for _ in range(c)]))
  rest=tuple(sorted([x for x,c in zip(items,counts) for _ in range(tail[x]-c)]))
  fac=prod(binomial(tail[x],c) for x,c in zip(items,counts))
  ans+=fac*mul(block(sub),mark(rest))
 return ans
parts={d:list(Partitions(d)) for d in range(N+1)}
monos={d:[prod(ks[i] for i in pa) for pa in parts[d]] for d in parts}
for g in [25]:
 ks[0]=P(2*g-2);block.cache_clear();mark.cache_clear()
 rows=[]
 for r in range(1,N+1):
  for s in range(max(0,3*r-g-1)+1):
   if s>3*r-g-1 or (r-g-1-s)%2:continue
   for sig in parts.get(s,list(Partitions(s))):
    if any(x%3==2 for x in sig):continue
    f=mul(sum(E),mark(tuple(sig)))
    f=P({m:c for m,c in f.dict().items() if sum((i+1)*a for i,a in enumerate(m))==r})
    for mon in monos[N-r]:rows.append(f*mon)
  print('g,r,rows',g,r,len(rows),flush=True)
 matrix=Matrix(F,[[f.monomial_coefficient(mon) for mon in monos[N]] for f in rows])
 print('RESULT',g,'part',len(parts[N]),'rank',matrix.rank(),'dim',len(parts[N])-matrix.rank(),flush=True)
 save(matrix,'fz25.sobj')
 @lru_cache(None)
 def integ(sig):
  # aggregate set partitions by their block sums
  @lru_cache(None)
  def blocks(s):
   if not s:return {():1}
   a=s[0]; tail=Counter(s[1:]); items=list(tail); out=Counter()
   for counts in cartesian_product([range(tail[x]+1) for x in items]):
    b=a+sum(x*c for x,c in zip(items,counts))
    rest=tuple(sorted(x for x,c in zip(items,counts) for _ in range(tail[x]-c)))
    fac=prod(binomial(tail[x],c) for x,c in zip(items,counts))
    for sums,v in blocks(rest).items():out[tuple(sorted((b,)+sums))]+=fac*v
   return dict(out)
  ans=F(0)
  for sums,c in blocks(sig).items():
   ans+=F(c)*(-1)**(len(sig)-len(sums))*F(factorial(2*g-3+len(sums)))/prod(F(prod(range(1,2*a+2,2))) for a in sums)
  return ans
 pairing=Matrix(F,[[integ(tuple(sorted(tuple(a)+tuple(b)))) for b in Partitions(g-2-N)] for a in parts[N]])
 print('PAIR RANK',pairing.rank(),'relations vanish?',(matrix*pairing).is_zero(),flush=True)
 save(pairing,'pair25.sobj')

# Try all one-pointed generalized FZ relations that push to degree 12.
N=13
T=PowerSeriesRing(QQ,'t',default_prec=N+1);t=T.gen()
A=T([QQ(factorial(6*n))/QQ(factorial(3*n)*factorial(2*n)) for n in range(N+1)])
B=T([QQ(factorial(6*n))*QQ(6*n+1)/QQ(factorial(3*n)*factorial(2*n)*(6*n-1)) for n in range(N+1)])
Q=B/A;L=A.log()
P=PolynomialRing(QQ,['k'+str(i) for i in range(1,N+1)]+['z'],implementation='generic');z=P.gen(N)
ks=[P(48)]+list(P.gens()[:N]);weights=list(range(1,N+1))+[1]
def trunc(f):return P({m:c for m,c in f.dict().items() if sum(a*b for a,b in zip(weights,m))<=N})
E=[P(1)]
for d in range(1,N+1):E.append(-sum(QQ(i)*L[i]*ks[i]*E[d-i] for i in range(1,d+1))/QQ(d))
@lru_cache(None)
def block(sig):
 shift=sum(x//3 for x in sig);nb=sum(x%3==1 for x in sig);S=t**shift*Q**nb
 return factorial(len(sig)-1)*sum(S[i]*(ks[i]+z**i) for i in range(N+1))
mark.cache_clear()
newrows=[]
for r in range(9,14):
 for a in [0,1]:
  for s in range(3*r-26-a+1):
   if (r-26-s-a)%2:continue
   for sig in Partitions(s):
    if any(x%3==2 for x in sig):continue
    f=mul(mul(sum(E),mark(tuple(sig))),sum((Q**a)[i]*z**i for i in range(N+1)))
    pushed={}
    for m,c in f.dict().items():
     if sum(x*y for x,y in zip(weights,m))!=r:continue
     exponent=m[N]+13-r
     if exponent<1:continue
     powers=list(m)[:N];coef=c
     if exponent==1:coef*=48
     else:powers[exponent-2]+=1
     key=tuple(powers[:12]);pushed[key]=pushed.get(key,0)+coef
    newrows.append([pushed.get(tuple(list(mon.exponents()[0])),0) for mon in monos[12]])
 print('POINTED',r,len(newrows),flush=True)
newmat=Matrix(QQ,newrows)
print('POINTED RANK',newmat.rank(),'COMBINED',matrix.stack(newmat).rank(),flush=True)

