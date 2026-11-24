src=open('workspace/jet_r2_agent4.py').read();src=src[:src.index('initial=')].replace('R=2','R=1').replace('@functools.lru_cache(None)\ndef push','@functools.lru_cache(120000)\ndef push');exec(src)
# Override subset coefficient using grouped multiplicities.
@functools.lru_cache(None)
def mergecoef(weights,b):
 co=Counter(weights);items=list(co.items());out=0
 for sel in itertools.product(*[range(n+1) for w,n in items]):
  size=sum(sel);total=sum(w*a for (w,n),a in zip(items,sel));mult=math.prod(math.comb(n,a) for (w,n),a in zip(items,sel))
  out+=(-1)**(len(weights)-size)*mult*pow(total,b,P)
 return (-1)**(b-len(weights))*out%P
fz={};fs=open('workspace/agent3_fz25.py').read();fs=fs[:fs.index('json.dump(dict')].replace('P=1000000007;','P=1000003;');exec(fs,fz)
import sympy as sy
EE={():1}
for j in range(1,13):
 c=(-1)**j*sy.bernoulli(j+1,R)/j/(j+1);c=int(sy.numer(c))*pow(int(sy.denom(c)),-1,P)%P
 FF={}
 for mon,v in EE.items():
  for a in range((12-sum(mon))//j+1):FF[tuple(sorted(mon+(j,)*a))]=v*pow(c,a,P)*pow(math.factorial(a),-1,P)%P
 EE=FF

def test(initial):
 raw=push(tuple(sorted(initial)));out=defaultdict(int)
 for a,u in raw.items():
  for b,v in EE.items():
   if sum(a+b)==12:out[tuple(sorted(a+b))]=(out[tuple(sorted(a+b))]+u*v)%P
 row=[out.get(m,0) for m in fz['basis']];original=row[:]
 for i,j in enumerate(fz['piv']):
  c=row[j];row=[(a-c*b)%P for a,b in zip(row,fz['M'][i])]
 nz=sum(bool(v) for v in row)
 print('TEST',initial,'residual',nz,'time',time.time()-start,flush=True)
 return nz,original

def partslen(n,k,lo=1):
 if k==0:
  if n==0:yield ()
 else:
  for x in range(lo,n//k+1):
   for tail in partslen(n-x,k-1,x):yield (x,)+tail
results=[]
for mass in range(12,23):
 for tail in partslen(mass,12):
  ini=[(x,0) for x in tail+(49-mass,)];nz,row=test(ini)
  results.append({'jets':[x for x,e in ini],'residual':nz,'row':row})
  json.dump(results,open('workspace/jet_canonical_smalltail_agent4.json','w'))
  if nz:raise Exception('EXTRA RELATION')
print('COMPLETE',len(results),'tests',time.time()-start)
