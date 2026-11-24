import json,pathlib,sys,collections,itertools,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
raw=json.loads(pathlib.Path('workspace/agent3_T280_P12_allorbits.json').read_text())['base_orbits']
v5=veronese(10,5);u5=veronese(11,5);u4=veronese(11,4);u6=veronese(11,6)
def flats(d):
 for piv in itertools.combinations(range(7),d):
  non=[j for j in range(7) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
  for z in range(1<<len(free)):
   B=[1<<p for p in piv]
   for h,(i,j) in enumerate(free):
    if z>>h&1:B[i]^=1<<j
   H=[0]
   for b in B:H += [x^b for x in H]
   offs=[0]
   for j in non:offs += [x^(1<<j) for x in offs]
   for off in offs:yield [x^off for x in H]
res=[];stats=[];hist=collections.Counter();bad=[];start=time.time()
for obj in raw:
 B=obj['base'];BS=set(B);S=sorted(x+(r<<7) for x in B for r in range(8));DD={}
 for j,p in enumerate(S):
  z=v5[p];c=1<<j
  while z:
   h=z.bit_length()-1
   if h in DD:z^=DD[h][0];c^=DD[h][1]
   else:DD[h]=(z,c);break
 for d in [1,2,3,4]:
  vv=veronese(7,d+1);D={}
  for p in B:
   z=vv[p]
   while z:
    h=z.bit_length()-1
    if h in D:z^=D[h]
    else:D[h]=z;break
  R=[]
  for p in range(128):
   z=vv[p]
   for h in sorted(D,reverse=True):
    if z>>h&1:z^=D[h]
   R.append(z)
  total=0;valid=0
  for Q in flats(d):
   total+=1
   if any(p in BS for p in Q):continue
   z=0
   for p in Q:z^=R[p]
   if z:continue
   valid+=1;P=sorted(x+(u<<7) for x in Q for u in range(1<<(4-d)));assert len(P)==16
   z=0
   for p in P:z^=v5[p]
   c=0
   while z:
    h=z.bit_length()-1;assert h in DD
    z^=DD[h][0];c^=DD[h][1]
   H=set(P)|{S[j] for j in range(256) if c>>j&1};F=sorted(H|{x^1024 for x in set(S)^H});assert len(F)==288
   syn=0
   for p in F:syn^=u6[p]
   assert syn==0
   K5=kernel(F,u5);K4=kernel(F,u4);odd=sum((a&b).bit_count()%2 for a in K4 for b in K5)
   hist[(d,len(K5),len(K4),bool(odd))]+=1
   rr={'type':obj['type'],'d':d,'Q':Q,'K5':len(K5),'K4':len(K4),'odd':odd}
   if odd:bad.append(dict(rr,support=F))
   res.append(rr)
  st={'type':obj['type'],'d':d,'total_flats':total,'valid':valid};stats.append(st);print(st,flush=True)
print('HIST',hist,'bad',len(bad),'secs',time.time()-start)
pathlib.Path('workspace/agent3_T288_E256_P16_affflats.json').write_text(json.dumps({'stats':stats,'histogram':{str(k):v for k,v in hist.items()},'results':res,'badseeds':bad},indent=2))
pathlib.Path('workspace/agent3_T288_E256_P16_affflats.py').write_text(pathlib.Path(__file__).read_text())
