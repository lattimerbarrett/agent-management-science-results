import z3,itertools,math,json,time
from pathlib import Path
configs=[((6,),(7,)),((3,3),(7,)),((6,),(3,4)),((3,3),(3,4)),((2,4),(3,4)),((3,3),(2,2,3))]
def xor(xs):
 if not xs:return z3.BoolVal(False)
 while len(xs)>1:xs=[z3.Xor(xs[i],xs[i+1]) if i+1<len(xs) else xs[i] for i in range(0,len(xs),2)]
 return xs[0]
results=[]
for uf,vf in configs:
 ns=uf+vf;nb=len(ns);points=list(itertools.product(*[range(n+1) for n in ns]));idx={a:i for i,a in enumerate(points)};N=len(points);weights=[math.prod(math.comb(n,b) for n,b in zip(ns,a)) for a in points];rows=[]
 for a in points:
  if sum(a)>=7:
   subs=list(itertools.product(*[[b for b in range(x+1) if b&x==b] for x in a]));mask=sum(1<<idx[b] for b in subs)
   if sum(a)>7:rows.extend([(mask,0),(mask<<N,0)])
   else:
    ga=int(all(a[i]==0 for i in range(len(uf))) and all(a[i]==ns[i] for i in range(len(uf),nb)))
    rows.append((mask|(mask<<N),ga))
 for i,w in enumerate(weights):
  if w>270:rows.extend([(1<<i,0),(1<<(i+N),0)])
 basis={};bad=False
 for row,rhs in rows:
  while row:
   p=row.bit_length()-1
   if p in basis:bb,rr=basis[p];row^=bb;rhs^=rr
   else:basis[p]=(row,rhs);break
  if not row and rhs:bad=True;break
 if bad:print('linear bad',ns);continue
 free=[i for i in range(2*N) if i not in basis];D=len(free);expr={i:1<<j for j,i in enumerate(free)}
 for p in sorted(basis):
  row,rhs=basis[p];row^=1<<p;v=rhs<<D
  while row:
   lo=row&-row;j=lo.bit_length()-1;v^=expr[j];row^=lo
  expr[p]=v
 s=z3.Solver();s.set(timeout=60000);bs=[z3.Bool('b%d'%j) for j in range(D)];f=[xor([b for j,b in enumerate(bs) if expr[i]>>j&1]+([z3.BoolVal(True)] if expr[i]>>D&1 else [])) for i in range(2*N)];H=f[:N];J=f[N:]
 weighted=list(zip(f,weights*2));s.add(z3.Or(*[z3.PbEq(weighted,w-64) for w in (322,326,330,334)]));s.add(z3.PbGe(list(zip(H,weights)),64));s.add(z3.PbLe(list(zip(H,weights)),135))
 # full-q along the two special directions: h dot j odd, g dot j odd
 s.add(xor([z3.And(H[i],J[i]) for i,w in enumerate(weights) if w%2]))
 s.add(xor([J[i] for i,a in enumerate(points) if all(a[j]==0 for j in range(len(uf),nb)) and weights[i]%2]))
 for block,n in enumerate(ns):
  terms=[]
  for a in itertools.product(*[range(nn+(i!=block)) for i,nn in enumerate(ns)]):
   if not all((aa&(nn-(i==block)))==aa for i,(nn,aa) in enumerate(zip(ns,a))):continue
   b=list(a);b[block]+=1;i=idx[a];j=idx[tuple(b)];terms.extend([z3.And(H[i],H[j]),z3.And(J[i],J[j])])
  s.add(xor(terms))
 tt=time.time();res=s.check();results.append((ns,D,str(res),time.time()-tt));print(results[-1],flush=True)
 if res==z3.sat:
  model=s.model();hv=[int(z3.is_true(model.eval(v))) for v in H];jv=[int(z3.is_true(model.eval(v))) for v in J];S=[]
  for x in range(1<<13):
   a=[];off=0
   for n in ns:a.append(((x>>off)&((1<<n)-1)).bit_count());off+=n
   i=idx[tuple(a)]
   if x>>6==0:S.append(x|(1<<13))
   if hv[i]:S.append(x|(1<<14))
   if jv[i]:S.append(x|(1<<13)|(1<<14))
  assert len(S) in (322,326,330,334)
  ss=set(S);arr=[int(x in ss) for x in range(1<<15)]
  for i in range(15):
   for x in range(1<<15):
    if x>>i&1:arr[x]^=arr[x^(1<<i)]
  assert max(x.bit_count() for x,v in enumerate(arr) if v)<=8
  json.dump({'ns':ns,'support':S},open('workspace/agent2_glue64_HIT.json','w'));print('VERIFIED HIT',len(S),flush=True);break
json.dump(results,open('workspace/agent2_glue64_results.json','w'));Path('workspace/agent2_glue64.py').write_text(Path(__file__).read_text())
