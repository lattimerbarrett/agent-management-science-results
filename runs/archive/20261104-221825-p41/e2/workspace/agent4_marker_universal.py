import z3,json,itertools,time
markers=json.load(open('workspace/agent2_orbit_shelling.json'))['markers'];N=len(markers)
M=z3.Int('m');f=[z3.Int('f%d'%i) for i in range(8)];D=M+2

def bounds(b):
 t=markers[b];S=list(t[1:3]) if t[0]=='e' else list(t[1:4]);lo=[0]*8;up=[z3.IntVal(0)]*8
 for i in S:lo[i]=1;up[i]=M
 if t[0]=='t':
  k=t[4];lo[k]=2
  for j in S:
   if j!=k and markers.index(['t',*S,j])<b:up[j]=z3.IntVal(1)
 return S,lo,up
B=[bounds(b) for b in range(N)]
def inside(b,x):
 S,lo,up=B[b]
 return z3.And(*[z3.And(x[i]>=lo[i],x[i]<=up[i]) for i in range(8)])
def compatible(b,r):
 S,lo,up=B[b];low=[z3.If(r[i]>lo[i],r[i],lo[i]) for i in range(8)]
 return z3.And(*[low[i]<=up[i] for i in range(8)],sum(low)<=D,sum(up)>=D)
results=[];start=time.time()
for b in range(N):
 S,lo,up=B[b]
 good=[]
 for i in range(8):
  opts=[]
  for j in range(8):
   if i==j:continue
   h=[f[k]-(i==k)+(j==k) for k in range(8)]
   opts.extend(inside(a,h) for a in range(b))
   if markers[b][0]=='t' and j==markers[b][4]:opts.append(inside(b,h))
  good.append(z3.Or(*opts))
 r=[z3.If(good[i],f[i],0) for i in range(8)]
 samehigher=z3.BoolVal(False)
 if markers[b][0]=='t':
  k=markers[b][4];_,bl,bu=B[b];lower=[z3.If(r[i]>bl[i],r[i],bl[i]) for i in range(8)];lower[k]=z3.If(lower[k]>f[k]+1,lower[k],f[k]+1)
  samehigher=z3.And(*[lower[i]<=bu[i] for i in range(8)],sum(lower)<=D,sum(bu)>=D)
 s=z3.Solver();s.add(M>=2,sum(f)==D,inside(b,f),z3.Or(samehigher,*[compatible(a,r) for a in range(b)]));s.set(timeout=10000)
 res=s.check()
 if res==z3.sat:
  model=s.model();v={'b':b,'marker':markers[b],'m':model[M].as_long(),'f':[model.eval(x).as_long() for x in f],'r':[model.eval(x).as_long() for x in r]};print('SAT',v,flush=True);results.append(v)
 elif res==z3.unknown:print('UNKNOWN',b,flush=True)
 else:print('UNSAT',b,flush=True)
 assert res==z3.unsat,(b,res)
json.dump({'blocks':N,'all_unsat':True,'elapsed':time.time()-start},open('workspace/agent4_marker_universal_result.json','w'));print('done',time.time()-start,len(results))
