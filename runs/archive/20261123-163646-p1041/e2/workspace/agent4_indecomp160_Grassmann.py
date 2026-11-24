from pathlib import Path
s=Path('workspace/agent4_higherorthogonal320_pipeline.py').read_text();exec(s[:s.index("D=json.loads")])
D=json.loads(Path('workspace/agent4_higherorthogonal320_pipeline.json').read_text());core=D[0]['found'][0]['support'];co=6;n=12;N=160;full=(1<<N)-1;S=[x|(rr<<11) for x in core for rr in range(2)];target=13;C=[full]+[sum(((x>>j)&1)<<i for i,x in enumerate(S)) for j in range(n)];r=5

def affsolve(rows,rhs,N):
 B={}
 for a,b in zip(rows,rhs):
  while a:
   p=a.bit_length()-1
   if p in B:a^=B[p][0];b^=B[p][1]
   else:B[p]=(a,b);break
  if not a and b:return None
 out=[];v=0
 for p in sorted(B):
  if ((B[p][0]&v).bit_count()^B[p][1])&1:v^=1<<p
 for j in range(N):
  if j in B:continue
  vv=1<<j
  for p in sorted(B):
   if (B[p][0]&vv).bit_count()&1:vv^=1<<p
  out.append(vv)
 return v,out

def extend2(D,target,N,r):
 BB=echelon(D)
 while len(D)<target:
  rows=list(products(D,r-1));rhs=[0]*len(rows)
  if len(D)==target-1:
   groups={}
   for j,pt in enumerate(points(D,N)):groups.setdefault(pt,[]).append(j)
   if max(map(len,groups.values()))>2:return None
   for g in groups.values():
    if len(g)==2:rows.append((1<<g[0])|(1<<g[1]));rhs.append(1)
  sol=affsolve(rows,rhs,N)
  if sol is None:return None
  v0,V=sol
  if len(V)<=len(D) and not reduce(BB,v0):return None
  for _ in range(30):
   v=v0^randomspan(V)
   if reduce(BB,v):break
  else:return None
  D.append(v);BB=echelon(D)
 return D

def key(C):
 B=echelon(C)
 for p in sorted(B):
  for q in B:
   if q>p and B[q]>>p&1:B[q]^=B[p]
 return tuple(B[p] for p in sorted(B))

start=time.time();hist=collections.Counter();cache={};accepted=0;found=[];best=0
for proposals in range(10000000):
 for _ in range(5):
  a,b=rng.sample(range(1,target),2);C[a]^=C[b]
 oldkey=key(C);drop=rng.choice([2,3,4,4,5,5,6]);keep=[full]+rng.sample(C[1:],target-1-drop);cand=extend2(keep,target,N,r)
 if cand is None:hist['dead']+=1
 else:
  newkey=key(cand)
  if newkey==oldkey:hist['same']+=1;C=cand
  else:
   if newkey not in cache:
    kd=N-len(echelon(products(cand,5)));pts=points(cand,N);pd=len(periods(pts)).bit_length()-1 if kd==1 else -1
    cache[newkey]=(kd,pd);hist['Kfull'+str(kd)]+=1
   kd,pd=cache[newkey]
   if kd!=1:hist['rejectdecomp']+=1
   else:
    C=cand;accepted+=1;hist['pd'+str(pd)]+=1
    if pd==0:
     pts=points(C,N);K=orth(products(C,4),N);gram=sum((a&b).bit_count()%2 for a in K for b in K)
     found.append({'support':sorted(pts),'C':C,'K4':len(K),'K5':1,'Gram':gram});print('INDECOMPAPERIODIC160',len(found),'K4',len(K),'Gram',gram,'proposal',proposals,'seconds',time.time()-start,flush=True)
     if len(found)>=20:break
 if time.time()-start>180:break
R={'proposals':proposals+1,'accepted':accepted,'distinct_codes':len(cache),'hist':dict(hist),'found':found,'seconds':time.time()-start};Path('workspace/agent4_indecomp160_Grassmann.json').write_text(json.dumps(R));Path('workspace/agent4_indecomp160_Grassmann.py').write_text(Path('scratchpad.py').read_text().split('