import itertools,json,random
open('workspace/a1_qshear.py','w').write(open(__file__).read())
random.seed(19)
N=1<<14; ALL=(1<<N)-1
X=[]
for i in range(14):
 block=(1<<(1<<i))-1
 # truth mask bit i =1
 s=0
 for j in range(1<<i,N,2<<i):s |=block<<j
 X.append(s)
ms=json.load(open('workspace/agent4_flat_seeds.json'))['320']
def points(mask):
 p=[0]
 for i in range(14):
  if mask>>i&1:p +=[x^(1<<i) for x in p]
 return p
def bits(p):return sum(1<<x for x in p)
base=0
for m in ms:base ^=bits(points(m))
def anf(b):
 a=bytearray((b>>x)&1 for x in range(N))
 for i in range(14):
  for x in range(N):
   if x>>i&1:a[x]^=a[x^(1<<i)]
 return [x for x,c in enumerate(a) if c]
def nullspace(rows,n):
 piv={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in piv:r^=piv[p]
   else:piv[p]=r;break
 free=[i for i in range(n) if i not in piv]; ans=[]
 for f in free:
  v=1<<f
  for p in sorted(piv):
   if (piv[p]&v).bit_count()%2:v ^=1<<p
  ans.append(v)
 return ans
# candidate affine flat directions neighboring original directions; count each alloffset via support
cand=set(ms)
for m in ms:
 for i in range(14):
  for j in range(14):
   if (m>>i&1) and not(m>>j&1):cand.add(m^(1<<i)^(1<<j))
cs=[((N-1)^m) for m in cand]
targets={322:63,326:61,330:59,334:57};found={}
def check(b,info):
 pp=[]
 while b:
  v=b&-b;pp.append(v.bit_length()-1);b^=v
 for c in cs:
  cnt={}
  for x in pp:
   p=x&c;cnt[p]=cnt.get(p,0)+1
  for goal,t in targets.items():
   if goal in found:continue
   for offset,num in cnt.items():
    if num==t:
     found[goal]={'shear':info,'flat_free':(N-1)^c,'flat_offset':offset}
     print('FOUND',goal,found[goal],flush=True)
     json.dump(found,open('workspace/a1_qshear_found.json','w'))
# Keep affine7-flat candidates with substantial initial overlap.
ppbase=[];temp=base
while temp:
 z=temp&-temp;ppbase.append(z.bit_length()-1);temp^=z
baseC=[]
for free in (sum(1<<j for j in c) for c in itertools.combinations(range(14),7)):
 constraint=(N-1)^free;ct={}
 for x in ppbase:ct[x&constraint]=ct.get(x&constraint,0)+1
 for off,num in ct.items():
  if num>=48:baseC.append([x^off for x in points(free)])
print('initial candidates',len(baseC),flush=True)
C=[]
for restart in range(100):
 b=base;C=[p[:] for p in baseC]
 for step in range(100):
  aa=anf(b);top=[m for m in aa if m.bit_count()==7]
  allchoices=[]
  for i in random.sample(list(range(14)),14):
   top6=[m^(1<<i) for m in top if m>>i&1]
   pairs=[(j,k) for j in range(14) for k in range(j+1,14) if i not in (j,k)]
   rows={}
   for col,(j,k) in enumerate(pairs):
    q=(1<<j)|(1<<k)
    for t in top6:
     if not t&q:rows[t|q]=rows.get(t|q,0)^(1<<col)
   ker=nullspace(rows.values(),len(pairs))
   if ker:allchoices.append((i,pairs,ker))
  if not allchoices:break
  i,pairs,ker=random.choice(allchoices)
  for attempt in range(50):
   v=0
   for z in ker:
    if random.randrange(2):v^=z
   qmask=0;qp=[]
   for col,(j,k) in enumerate(pairs):
    if v>>col&1:qmask ^=X[j]&X[k];qp.append([j,k])
   swap0=((b&X[i])>>(1<<i))|((b&(ALL^X[i]))<<(1<<i))
   nonlinear_changed=bool((b^swap0)&qmask)
   linear=0
   for j in range(14):
    if j!=i and random.randrange(2):qmask ^=X[j];qp.append([j]);linear ^=1<<j
   constant=random.randrange(2)
   if constant:qmask ^=ALL;qp.append([])
   swap=((b&X[i])>>(1<<i))|((b&(ALL^X[i]))<<(1<<i))
   bb=b^((b^swap)&qmask)
   if bb!=b:
    assert bb.bit_count()==320
    C=[[x^((((x&linear).bit_count()%2)^constant)<<i) for x in p] for p in C]
    for p in C:
     tt=(bb&bits(p)).bit_count()
     if tt in targets.values():
      goal=448-2*tt
      if goal not in found:
       support=bb^bits(p)
       found[goal]={'support':hex(support),'flat':p}
       print('FOUND TRACKED',goal,flush=True)
       json.dump(found,open('workspace/a1_qshear_found.json','w'))
    check(bb,{'restart':restart,'step':step,'i':i,'q':qp,'before':hex(b)})
    b=bb;break
  if step%50==0:print('step',restart,step,'ker',len(ker),'nonlinear',nonlinear_changed,'found',list(found),flush=True)
  if len(found)==4:break
 if len(found)==4:break
print('DONE',found.keys())