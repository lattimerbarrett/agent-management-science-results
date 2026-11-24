from pathlib import Path
exec(Path('workspace/agent4_allcorrected.py').read_text().split('for g in range(1,13):')[0])
import pickle,json,time
from sage.all import bernoulli
Ed=json.load(open('workspace/fz25_exceptional.json'));E=[(tuple(a),int(v)%P) for a,v in zip(Ed['basis'],Ed['vector'])]
@lru_cache(None)
def fact(h,d):return pickle.load(open('workspace/agent2_exactfactor_%02d_%02d.pkl'%(h,d),'rb'))
def boundary_value(g,h,x,y):
 I,t=x;J,u=y;out=0
 for p,c in E:
  v=0
  for a,b,z in splits(p):
   if sum(a)+sum(I)+t!=g-1:continue
   va=1 if g==1 else point(tuple(sorted(a+I,reverse=True)),t,g)
   v+=z*va*point(tuple(sorted(b+J,reverse=True)),u,h)
  out+=c*(v%P)
 return out%P
T=lambda k:F(abs(bernoulli(2*k)))/F(2**(2*k-1)*factorial(2*k))
answer=F(0);contrib=[]
for g in range(1,13):
 h=25-g;t0=time.time();sol=pickle.load(open('workspace/agent2_exact_divisibility_%02d.pkl'%g,'rb'));ans=F(0)
 for v,(d,x,y) in zip(sol['solution'],sol['domain']):
  if not v:continue
  a=fact(g,d);b=fact(h,11-d)
  xx=a['basis'][a['free'][x]];yy=b['basis'][b['free'][y]]
  ans+=F(v)*boundary_value(g,h,xx,yy)
 ans*=T(g)*T(h);answer+=ans;contrib.append(int(ans))
 print('split',g,int(ans),'time',time.time()-t0,flush=True)
assert int(answer)==296879567
print('ACTUAL EXACT-Q BOUNDARY SCALAR VERIFIED',int(answer),flush=True)
json.dump({'p':P,'scalar':int(answer),'split_contributions':contrib},open('workspace/agent4_boundary_good_actualQ.json','w'))
