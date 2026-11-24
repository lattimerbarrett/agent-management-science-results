import z3,time,json,itertools,pathlib
pathlib.Path('workspace/agent4_normalized_span14_sat.py').write_text(pathlib.Path(__file__).read_text())
start=time.time(); n=14; N=1<<n
s=z3.With(z3.Tactic('sat'),anf=True,**{'anf.exlin':True,'cardinality.solver':True}).solver();s.set(timeout=600000)
f=[z3.Bool('f_%d'%i) for i in range(N)];a=f[:]
for j in range(n):
 bit=1<<j
 for x in range(N):
  if x&bit:
   t=z3.Bool('a_%d_%d'%(j,x));s.add(t==z3.Xor(a[x],a[x^bit]));a[x]=t
for x in range(N):
 if x.bit_count()>8:s.add(z3.Not(a[x]))
s.add(a[255])
for j in range(8):
 mask=255^(1<<j);s.add(a[mask])
 for b in range(6):s.add(z3.Not(a[mask|(1<<(8+b))]))
for b in [0,1,2,3,4,8,16]:
 s.add(f[b<<8])
 for z in range(1,256):s.add(z3.Not(f[(b<<8)|z]))
for ell in range(1,256):s.add(z3.Or([f[(b<<8)|z] for b in range(64) for z in range(1,256) if (ell&z).bit_count()%2]))
s.add(z3.PbLe([(v,1) for v in f],156))
def xor(xs):
 t=z3.BoolVal(False)
 for x in xs:t=z3.Xor(t,x)
 return t
inds=list(itertools.combinations(range(8),2));idx={p:i for i,p in enumerate(inds)}
def pfaff(v,mat):
 if not v:return z3.BoolVal(True)
 q=v[0]
 return xor([z3.And(mat[idx[(q,v[i])]],pfaff(v[1:i]+v[i+1:],mat)) for i in range(1,len(v))])
terms=[]
for b in range(64):
 row=f[b<<8:(b+1)<<8];s.add(z3.Or(row))
 t=z3.Bool('nontriv_%d'%b);s.add(t==z3.Or(row[1:]));u=z3.Bool('contains0defect_%d'%b);s.add(u==z3.And(t,row[0]))
 vals=[]
 for i,j in inds:
  mask=255^(1<<i)^(1<<j);coeff=[a[(q<<8)|mask] for q in range(64) if q.bit_count()<=2 and b&q==q]
  v=z3.Bool('M_%d_%d_%d'%(b,i,j));s.add(v==z3.Not(xor(coeff)));vals.append(v)
 d=z3.Bool('null2defect_%d'%b);s.add(d==z3.And(t,z3.Not(z3.Or(vals))))
 r4=z3.Bool('rank4_%d'%b);s.add(r4==z3.Or([pfaff(list(v),vals) for v in itertools.combinations(range(8),4)]))
 r6=z3.Bool('rank6_%d'%b);s.add(r6==z3.Or([pfaff(list(v),vals) for v in itertools.combinations(range(8),6)]))
 r8=z3.Bool('rank8_%d'%b);s.add(r8==pfaff(list(range(8)),vals))
 terms.extend([(t,1),(u,1),(d,2),(r4,1),(r6,1),(r8,1)])
s.add(z3.PbLe(terms,46))
print('built',time.time()-start,flush=True)
r=s.check();print(r,time.time()-start,flush=True)
result={'result':str(r),'seconds':time.time()-start,'meaning':'normalized odd-fiber RM(8,14), wt<=156, full affine span14'}
if r==z3.sat:
 model=s.model();supp=[i for i,v in enumerate(f) if z3.is_true(model.eval(v))];result['support']=supp
 S=set(supp);arr=[int(i in S) for i in range(N)]
 for j in range(n):
  for x in range(N):
   if x&(1<<j):arr[x]^=arr[x^(1<<j)]
 assert max((x.bit_count() for x,v in enumerate(arr) if v),default=0)<=8
 assert len(supp)<=156
 for b in range(64):
  row=[z for z in range(256) if ((b<<8)|z) in S]
  assert len(row)%2==1
  zz=0
  for z in row:zz^=z
  assert zz==0
if r==z3.unknown:result['reason']=s.reason_unknown()
pathlib.Path('workspace/agent4_normalized_span14_sat_status.json').write_text(json.dumps(result,indent=2));print(result)
