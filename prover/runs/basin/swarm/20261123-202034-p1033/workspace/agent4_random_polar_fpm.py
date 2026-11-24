import itertools,time,json,random,numpy as np
from scipy.optimize import linprog
start=time.time();rng=random.Random(89765)
def mincovers(H,n,r):
 return [sum(1<<v for v in C) for C in itertools.combinations(range(n),r) if all(sum(1<<v for v in C)&e for e in H)]
def compress(H):
 verts=[v for v in range(max(H).bit_length()) if any(e>>v&1 for e in H)]
 return [sum(1<<i for i,v in enumerate(verts) if e>>v&1) for e in H],len(verts)
def normalize(H,n,r):
 while True:
  B=mincovers(H,n,r);pairset=set()
  for c in B:
   pairset.update(itertools.combinations([v for v in range(n) if c>>v&1],2))
  missing=[(v,w) for v,w in itertools.combinations(range(n),2) if (v,w) not in pairset]
  if not missing:return H,n,B
  v,w=rng.choice(missing)
  H=list(set((e&~(1<<w))|((1<<v) if e>>w&1 else 0) for e in H));H,n=compress(H)
res=[];counter=None
for r,n,trials in [(3,7,100),(3,8,100),(4,9,200),(4,10,200),(5,11,200),(5,12,200)]:
 allE=[sum(1<<v for v in C) for C in itertools.combinations(range(n),r)];covers=[sum(1<<v for v in C) for C in itertools.combinations(range(n),r-1)]
 good=0;fpm=0;ns={}
 for trial in range(trials):
  order=allE[:];rng.shuffle(order);H=[]
  for e in order:
   if all(e&f for f in H):H.append(e)
  if any(all(c&e for e in H) for c in covers):continue
  good+=1;H,N=compress(H);H,N,B=normalize(H,N,r)
  assert not any(all(c&e for e in H) for c in [sum(1<<v for v in C) for C in itertools.combinations(range(N),r-1)])
  A=np.array([[int(c>>v&1) for c in B] for v in range(N)],dtype=float)
  lp=linprog(np.zeros(len(B)),A_eq=A,b_eq=np.ones(N),bounds=(0,None),method='highs')
  ns[N]=ns.get(N,0)+1
  if lp.success:fpm+=1
  else:
   counter=dict(r=r,n=N,H=[[v for v in range(N) if e>>v&1] for e in H],B=[[v for v in range(N) if c>>v&1] for c in B]);print('COUNTER',counter,flush=True);break
 item=dict(r=r,initial_n=n,trials=trials,tau_r_count=good,fpm_count=fpm,orders=ns);res.append(item);print(item,'time',time.time()-start,flush=True)
 if counter:break
with open('workspace/agent4_random_polar_fpm.json','w') as f:json.dump(dict(results=res,counter=counter),f,indent=2)
with open('workspace/agent4_random_polar_fpm.py','w') as f:f.write(open(__file__).read())
