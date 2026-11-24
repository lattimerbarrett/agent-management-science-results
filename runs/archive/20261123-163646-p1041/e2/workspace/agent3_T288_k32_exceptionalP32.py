import itertools,json,pathlib,sys,collections,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
raw=json.loads(pathlib.Path('workspace/agent3_P32_E32_quadrics.json').read_text())
def bas(vals):
 D={}
 for z in vals:
  while z:
   h=z.bit_length()-1
   if h in D:z^=D[h]
   else:D[h]=z;break
 return list(D.values())
def subspaces(r,j):
 for piv in itertools.combinations(range(r),j):
  free=[(i,k) for i,p in enumerate(piv) for k in range(p+1,r) if k not in piv]
  for bits in range(1<<len(free)):
   B=[1<<p for p in piv]
   for z,(i,k) in enumerate(free):
    if bits>>z&1:B[i]|=1<<k
   yield B
def solve(rows):
 D={}
 for a,b in rows:
  while a:
   h=a.bit_length()-1
   if h in D:a^=D[h][0];b^=D[h][1]
   else:D[h]=(a,b);break
  if not a and b:return None
 z=0
 for h,(a,b) in sorted(D.items()):
  if ((a&z).bit_count()%2)^b:z^=1<<h
 assert all(((a&z).bit_count()%2)==b for a,b in rows)
 return z
def qG(x):return sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(3))&1
mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(9),k)];vv=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
T=[x for x in range(512) if qG(x)];assert len(kernel(T,veronese(9,5)))==10
v3=veronese(10,3);v5=veronese(10,5);v6=veronese(10,6)
results=[];hist=collections.Counter();total=0;start=time.time()
for obj in raw:
 B=obj['base'];before=total
 for case in obj['cases']:
  q=case['q'];t=case['t'];r=case['r'];assert not case['rad_nonzero'] and case['arf']==0
  def pol(a,b):return q[a^b]^q[a]^q[b]
  remaining=list(range(128));pairs=[]
  for _ in range(t):
   uv=next((a,b) for a in remaining if a and not q[a] for b in remaining if not q[b] and pol(a,b))
   a,b=uv;pairs += [a,b];remaining=[x for x in remaining if not pol(x,a) and not pol(x,b)]
  assert set(remaining)==set(case['rad'])
  R=bas(remaining);assert len(R)==r
  def cv(a):
   z=0
   for k,b in enumerate(R):
    if a>>k&1:z^=b
   return z
  for j in ([2,3] if t==2 else [3]):
   for J in subspaces(r,j):
    ext=J[:];comp=[]
    for i in range(r):
     if len(bas(ext+[1<<i]))>len(ext):ext.append(1<<i);comp.append(1<<i)
    src=pairs+[cv(a) for a in J]+[cv(a) for a in comp]
    tar=[1<<i for i in range(2*t)]+[1<<(6+i) for i in range(j)]+[1<<(2*t+2*i) for i in range(len(comp))]
    assert len(src)==len(tar)==7 and len(bas(src))==len(bas(tar))==7
    mp={0:0}
    for a,b in zip(src,tar):mp.update({x^a:y^b for x,y in list(mp.items())})
    assert len(mp)==128 and all(qG(y)==q[x] for x,y in mp.items())
    P={mp[x] for x in B};assert len(P)==32 and all(not qG(x) for x in P)
    sol=solve([(vv[x],int(x in P)) for x in range(512) if not qG(x)]);total+=1
    if sol is None:continue
    H={x for x in range(512) if (vv[x]&sol).bit_count()%2};F=sorted(H|{x^512 for x in set(T)^H});assert len(F)==288
    sy=0
    for p in F:sy^=v6[p]
    assert sy==0
    K3=kernel(F,v3);K5=kernel(F,v5);odd=sum((a&b).bit_count()%2 for a in K3 for b in K5)
    hist[(len(K3),len(K5),bool(odd))]+=1
    results.append({'type':obj['type'],'poly':case['poly'],'t':t,'j':j,'J':J,'P':sorted(P),'support':F,'K3':len(K3),'K5':len(K5),'odd':odd})
 print(obj['type'],'cases',total-before,'valid_cumulative',len(results),'secs',time.time()-start,flush=True)
print('TOTAL',total,'valid',len(results),'HIST',hist)
pathlib.Path('workspace/agent3_T288_k32_exceptionalP32.json').write_text(json.dumps({'cases':total,'histogram':{str(k):v for k,v in hist.items()},'results':results},indent=2))
pathlib.Path('workspace/agent3_T288_k32_exceptionalP32.py').write_text(pathlib.Path(__file__).read_text())
