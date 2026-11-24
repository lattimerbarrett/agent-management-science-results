import json,pathlib,itertools,collections
raw=json.loads(pathlib.Path('workspace/agent3_T280_P12_allorbits.json').read_text())['base_orbits']
mons=[sum(1<<j for j in I) for k in range(3) for I in itertools.combinations(range(7),k)]
vec=[sum(1<<j for j,M in enumerate(mons) if p&M==M) for p in range(128)]
def null(rows,n):
 D={}
 for z in rows:
  while z:
   p=z.bit_length()-1
   if p in D:z^=D[p]
   else:D[p]=z;break
 out=[]
 for i in range(n):
  if i in D:continue
  z=1<<i
  for p in sorted(D):
   if (D[p]&z).bit_count()%2:z^=1<<p
  out.append(z)
 return out
out=[]
for obj in raw:
 B=sorted(x^obj['base'][0] for x in obj['base']);K=null([vec[p] for p in B],29);assert len(K)==5
 hist=collections.Counter();cases=[]
 for z in range(1,32):
  c=0
  for i,k in enumerate(K):
   if z>>i&1:c^=k
  q=[(vec[p]&c).bit_count()%2 for p in range(128)];assert not q[0]
  BM=[sum((q[(1<<i)^(1<<j)]^q[1<<i]^q[1<<j])<<i for i in range(7)) for j in range(7)]
  rad=[p for p in range(128) if all((b&p).bit_count()%2==0 for b in BM)];r=(len(rad)).bit_length()-1;t=(7-r)//2;l=any(q[p] for p in rad)
  eps=None if l else int(sum(q)>64)
  hist[(t,r,l,eps)]+=1;cases.append({'poly':c,'q':q,'rad':rad,'t':t,'r':r,'rad_nonzero':l,'arf':eps})
 print(obj['type'],hist)
 out.append({'type':obj['type'],'base':B,'cases':cases})
pathlib.Path('workspace/agent3_P32_E32_quadrics.json').write_text(json.dumps(out,indent=2))
pathlib.Path('workspace/agent3_P32_E32_quadrics.py').write_text(pathlib.Path(__file__).read_text())
