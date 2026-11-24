import numpy as np,itertools,time,json,z3
m=13;n=1<<m;start=time.time();parent=list(range(n))
def root(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
def union(a,b):
 a=root(a);b=root(b)
 if a!=b:parent[max(a,b)]=min(a,b)
def bitperm(x,p):return sum(((x>>i)&1)<<p[i] for i in range(m))
# Orthogonal q=x0x1+x2x3 transformations, including a linear shear.
gens=[]
for p in [[1,0,2,3]+list(range(4,13)),[0,1,3,2]+list(range(4,13)),[2,3,0,1]+list(range(4,13))]:gens.append(lambda x,p=p:bitperm(x,p))
gens.append(lambda x:x^(((x>>2)&1)<<0)^(((x>>1)&1)<<3))
for off,k in [(4,4),(8,5)]:
 for mode in [0,1]:
  p=list(range(m))
  for i in range(k):p[off+i]=off+((i+1)%k if mode==0 else (1-i if i<2 else i))
  gens.append(lambda x,p=p:bitperm(x,p))
for fn in gens:
 for x in range(n):union(x,fn(x))
roots=[root(x) for x in range(n)];reps=sorted(set(roots));idx={x:i for i,x in enumerate(reps)};orb=[idx[x] for x in roots];sizes=[0]*len(reps)
for j in orb:sizes[j]+=1
N=len(reps);print('orbits',N,flush=True)
g=np.array([((x&1)*((x>>1)&1)^((x>>2)&1)*((x>>3)&1)) if x>>8==0 else 0 for x in range(n)],dtype=np.uint8);assert int(g.sum())==96
anfg=g.copy()
for i in range(m):
 a=anfg.reshape(-1,2**(i+1));a[:,2**i:]^=a[:,:2**i]
# Build full coefficient rows by Möbius transform of orbit unit vectors.
vec=[1<<j for j in orb]
for i in range(m):
 b=1<<i
 for x in range(n):
  if x&b:vec[x]^=vec[x^b]
rows=[]
for x in range(n):
 d=x.bit_count()
 if d>7:rows.extend([(vec[x],0),(vec[x]<<N,0)])
 elif d==7:rows.append((vec[x]^(vec[x]<<N),int(anfg[x])))
for j,sz in enumerate(sizes):
 if sz>238:rows.extend([(1<<j,0),(1<<(j+N),0)])
B={};R={}
for v,rhs in rows:
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k];rhs^=R[k]
  else:B[k]=v;R[k]=rhs;break
 if not v:assert rhs==0
part=0
for k in sorted(B):
 if ((B[k]&part).bit_count()%2)^R[k]:part^=1<<k
null=[]
for j in range(2*N):
 if j in B:continue
 v=1<<j
 for k in sorted(B):
  if (B[k]&v).bit_count()%2:v^=1<<k
 null.append(v)
print('free',len(null),'time',time.time()-start,flush=True)
def bx(v):
 if not v:return z3.BoolVal(False)
 while len(v)>1:v=[z3.Xor(v[i],v[i+1]) if i+1<len(v) else v[i] for i in range(0,len(v),2)]
 return v[0]
s=z3.Tactic('sat').solver();s.set(timeout=90000,anf=True,**{'anf.exlin':True,'anf.delay':0});v=[z3.Bool(f'v{i}') for i in range(len(null))];out=[]
for j in range(2*N):
 q=bx([v[k] for k,b in enumerate(null) if b>>j&1]);out.append(z3.Not(q) if part>>j&1 else q)
targets=[258,260,262,264,266,268,270,274,276,278,280,282,284,286,290,292,294,298,300,302,306,310,322,326,330,334]
s.add(z3.PbEq([(out[j],sizes[j]) for j in range(N)],96),z3.Or(*[z3.PbEq([(out[N+j],sizes[j]) for j in range(N)],ww) for ww in [130,134,138,142]]));ans=s.check();print('RESULT',ans,'time',time.time()-start,flush=True)
if ans==z3.sat:
 model=s.model();word=part
 for b,q in zip(null,v):
  if z3.is_true(model.eval(q,model_completion=True)):word^=b
 h=np.array([(word>>orb[x])&1 for x in range(n)],dtype=np.uint8);j=np.array([(word>>(N+orb[x]))&1 for x in range(n)],dtype=np.uint8)
 f=np.concatenate([np.zeros(n,dtype=np.uint8),g,h,j]);S=np.where(f)[0].tolist();a=f.copy()
 for i in range(15):
  b=a.reshape(-1,2**(i+1));b[:,2**i:]^=b[:,:2**i]
 deg=max(int(x).bit_count() for x in np.where(a)[0]);print('FOUND',len(S),'degree',deg,flush=True);assert deg<=8
 json.dump({'weight':len(S),'support':S,'g_weight':96,'h_weight':int(h.sum()),'j_weight':int(j.sum())},open('workspace/agent1_gluing96_found.json','w'))
