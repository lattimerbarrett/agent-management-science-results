from pathlib import Path
s=Path('workspace/agent2_boundary_functional25.py').read_text().split('# Independent direct string recursion')[0]
exec(s)
from sage.all import GF,matrix,vector
import random,itertools,json,time
random.seed(12345)
F=GF(P)
def partitions(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in partitions(n-a,a):yield (a,)+t
@lru_cache(None)
def l1(h,ks,e):
 assert sum(ks)+e==h-1
 if h==1:return 1
 scale=pow(invdf[h-2]*fact[2*h-2]%P,P-2,P)
 q=poly(ks);D=sum(ks)
 if e:return sum(a*fact[2*h-2+m] for m,a in enumerate(q))%P*invdf[e-1]%P*scale%P
 return sum(a*fact[2*h-3+m]*(2*D+m) for m,a in enumerate(q))%P*scale%P
parts12=list(partitions(12));tests=[[(ks,d-sum(ks)) for k in range(d+1) for ks in partitions(k)] for d in range(12)]
splits=[]
for ks in parts12:
 vals=sorted(set(ks));cs=[ks.count(x) for x in vals];out=[[] for j in range(13)]
 for ns in itertools.product(*(range(c+1) for c in cs)):
  aa=[];bb=[];cf=1
  for x,c,n in zip(vals,cs,ns):aa +=[x]*n;bb +=[x]*(c-n);cf*=comb(c,n)
  out[sum(aa)].append((tuple(aa),tuple(bb),cf))
 splits.append(out)
rows=[];labels=[];E={};start=time.time()
def row(h,j,left,right):
 aa,e=left;bb,f=right
 return [sum(cf*l1(h,tuple(sorted(a+aa)),e)*l1(25-h,tuple(sorted(b+bb)),f) for a,b,cf in ss[j])%P for ss in splits]
def add(r):
 r=list(r)
 for piv,rr in E.items():
  if r[piv]:
   z=r[piv];r=[(x-z*y)%P for x,y in zip(r,rr)]
 p=next((i for i,x in enumerate(r) if x),None)
 if p is None:return False
 iv=pow(r[p],P-2,P);r=[x*iv%P for x in r];E[p]=r
 return True
for h in range(1,13):
 for trial in range(500):
  j=random.randrange(min(h-1,12)+1);u=h-1-j;v=11-u
  if not 0<=v<=11:continue
  aa=random.choice(tests[u]);bb=random.choice(tests[v]);r=row(h,j,aa,bb)
  if add(r):rows.append(r);labels.append((h,j,aa,bb))
  if len(E)==77:break
 print('split',h,25-h,'rank',len(E),'seconds',time.time()-start,flush=True)
 if len(E)==77:break
print('numericalboundaryconstraintkernel',77-len(E),flush=True)
json.dump({'monomials':parts12,'rows':rows,'labels':labels,'prime':P},open('workspace/agent2_lambda25lambda23_boundary.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_lambda25lambda23_boundary.py').write_text(Path(__file__).read_text())
