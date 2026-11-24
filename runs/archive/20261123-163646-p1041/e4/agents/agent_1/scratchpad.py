import random,math,time,json
random.seed(1734);D=4;ALL=(1<<16384)-1;V=[sum(1<<x for x in range(16384)if x>>j&1)for j in range(14)]+[ALL];LC={0:0}
def lin(mask):
 if mask not in LC:LC[mask]=lin(mask&(mask-1))^V[(mask&-mask).bit_length()-1]
 return LC[mask]
IDENT=[ALL*int(i==j)for i in range(D)for j in range(D)]
def mm(A,B):return [__import__('functools').reduce(int.__xor__,(A[D*i+k]&B[D*k+j]for k in range(D)))for i in range(D)for j in range(D)]
def trace(Q):
 P=IDENT
 for M in Q:P=mm(P,list(map(lin,M)))
 f=0
 for i in range(D):f^=P[D*i+i]
 return f
need={310,322,326,330,334};found={};start=time.time();steps=0;best=999
for restart in range(500):
 Q=[[0]*(D*D)for _ in range(7)]
 for i in range(7):Q[i][0]=1<<i;Q[i][D+1]=1<<(7+i)
 for _ in range(random.randrange(8,25)):Q[random.randrange(7)][random.randrange(D*D)]^=1<<random.randrange(15)
 f=trace(Q);w=f.bit_count();target=random.choice(list(need));E=abs(w-target)+(30 if w%4!=2 else 0)
 for stage in range(30):
  # neutral gauges
  for _ in range(5):
   i=random.randrange(7);j=(i+1)%7;a,b=random.sample(range(D),2)
   for r in range(D):Q[i][D*r+b]^=Q[i][D*r+a]
   for c in range(D):Q[j][D*a+c]^=Q[j][D*b+c]
  if stage%3==2:
   a,b=random.sample(range(14),2)
   for M in Q:
    for j in range(D*D):
     if M[j]>>a&1:M[j]^=1<<b
   nf=trace(Q);assert nf.bit_count()==w;f=nf
  i=random.randrange(7);P=IDENT
  for t in range(1,7):P=mm(P,list(map(lin,Q[(i+t)%7])))
  delta=[P[D*b+a]&V[k]for a in range(D)for b in range(D)for k in range(15)]
  T=max(.3,30*(1-stage/30))
  for inner in range(1000):
   z=random.randrange(D*D*15);df=delta[z];nf=f^df;nw=nf.bit_count();ne=abs(nw-target)+(30 if nw%4!=2 else 0)
   if ne<=E or random.random()<math.exp((E-ne)/T):Q[i][z//15]^=1<<(z%15);f=nf;w=nw;E=ne
   steps+=1
   if w in need:
    print('FOUND',w,'restart',restart,'stage',stage,'steps',steps,'time',time.time()-start,flush=True);assert trace(Q)==f
    support=[x for x in range(16384)if f>>x&1];found[w]={'Q':Q,'support':support};json.dump(found,open('workspace/a1_width4_hard.json','w'));need.remove(w)
    if not need:break
    target=random.choice(list(need));E=abs(w-target)+(30 if w%4!=2 else 0)
  if not need:break
 if restart%50==0:print('restart',restart,'need',need,'steps',steps,'time',time.time()-start,flush=True)
 if not need:break
print('DONE',need,'steps',steps,'time',time.time()-start)
