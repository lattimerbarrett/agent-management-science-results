import sys,itertools,random,time
sys.path.insert(0,'workspace')
from agent4_checker import dec
random.seed(291)
for sizes,trials in [((2,2,2,2,2),500),((3,3,2,2,2),500)]:
 parts=[];n=0
 for s in sizes:parts.append(list(range(n,n+s)));n+=s
 initial={sum(1<<v for v in c) for c in itertools.product(*parts)}
 tests=0
 for trial in range(trials):
  D=set(initial)
  while True:
   faces={0}
   for f in D:
    q=f
    while q:faces.add(q);q=(q-1)&f
   options=[]
   for u,v in itertools.combinations(range(n),2):
    sigma=(1<<u)|(1<<v)
    if sigma in faces:continue
    triangles=[sum(1<<i for i in c) for c in itertools.combinations([i for i in range(n) if i not in (u,v)],3) if (sum(1<<i for i in c)|(1<<u)) in faces and (sum(1<<i for i in c)|(1<<v)) in faces]
    if triangles:options.append((sigma,triangles))
   if not options:break
   sigma,triangles=random.choice(options)
   t=random.choice(triangles);chosen=[t]
   Lfaces={0};q=t
   while q:Lfaces.add(q);q=(q-1)&t
   for j in range(random.randint(1,25)):
    available=[]
    for F in triangles:
     if F in chosen:continue
     R=0
     for i in range(n):
      if F>>i&1 and F^(1<<i) in Lfaces:R|=1<<i
     if R not in Lfaces and R.bit_count()<=2:available.append(F)
    if not available:break
    F=random.choice(available);chosen.append(F);q=F
    while q:Lfaces.add(q);q=(q-1)&F
   D.update(sigma|t for t in chosen)
   sk=tuple(sorted({f^(1<<i) for f in D for i in range(n) if f>>i&1}))
   tests+=1
   if not dec(sk,0):
    print('SMOOTHING COUNTER dim4',n,tuple(sorted(D)),flush=True);raise SystemExit
 print('PASS general edge decomposition dim4',sizes,tests,flush=True)
open('workspace/agent2_edge_stress_dim4.py','w').write(open(__file__).read())
