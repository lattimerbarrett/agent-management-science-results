import numpy as np,itertools,random,time,json
NN=4096;monoms=[m for m in range(NN) if m.bit_count()<=4];allx=np.arange(NN,dtype=np.uint16);mma=np.array(monoms,dtype=np.uint16)[:,None];Eval=((allx[None,:]&mma)==mma).astype(np.uint8)
def span(vecs,shift=0):
 p=[shift]
 for v in vecs:p += [x^v for x in p]
 return p
def bm(ps):return sum(1<<x for x in ps)
rowvals=[r for r in range(16) if ((r&1)*((r>>1)&1)^((r>>2)&1)*((r>>3)&1))];assert len(rowvals)==6
Dpts=[r+(y<<4) for r in rowvals for y in range(32)];d=bm(Dpts);assert d.bit_count()==192
Y=[bm([r*32+y for r in range(6) for y in range(32) if y>>i&1]) for i in range(5)]
base=[]
for i in range(5):
 for j in range(i):base.append(Y[i]&Y[j])
for i in range(5):
 for j in range(5):
  v=bm([r*32+y for r in range(6) for y in range(32) if y>>i&1 and (True if j==4 else rowvals[r]>>j&1)])
  base.append(v)
for r in range(6):base.append(((1<<32)-1)<<(32*r))
assert len(base)==41
ALL32=(1<<32)-1;ys=[sum(1<<y for y in range(32) if y>>i&1) for i in range(5)];faces=[(i,j,ys[i]&ys[j],(ALL32^ys[i])&(ALL32^ys[j])) for i in range(5) for j in range(i)]

def decode(h):
 hs=[(h>>(32*r))&ALL32 for r in range(6)];q=0
 for i,j,truth,mask in faces:
  cnt=sum(((v^(v>>(1<<i))^(v>>(1<<j))^(v>>((1<<i)+(1<<j))))&mask).bit_count() for v in hs)
  if cnt>24:q^=truth
 rem=[v^q for v in hs];coeff=[]
 for v in rem:
  coeff.append(sum(int(((v^(v>>(1<<i)))&(ALL32^ys[i])).bit_count()>8)<<i for i in range(5)))
 for heavy in range(6):
  cc=coeff.copy();cc[heavy]=0
  for r in range(6):
   if r!=heavy:cc[heavy]^=cc[r]
  out=0
  for r in range(6):
   aff=0
   for i in range(5):
    if cc[r]>>i&1:aff^=ys[i]
   if (rem[r]^aff).bit_count()>16:aff^=ALL32
   out|=(q^aff)<<(32*r)
  err=h^out
  if err.bit_count()<=15:return out,err
 return None
for _ in range(1000):
 q=0
 for b in base:
  if random.getrandbits(1):q^=b
 err=bm(random.sample(range(192),random.randrange(16)));ans=decode(q^err);assert ans and ans[1]==err
print('decoder1000randomtestsPASSED',flush=True)

def image(V,Dpts):
 inds={x:i for i,x in enumerate(V)};packed=np.packbits(Eval[:,V],axis=1,bitorder='little');rows=[int.from_bytes(r.tobytes(),'little') for r in packed];piv={}
 for row in rows:
  while row:
   p=row.bit_length()-1
   if p in piv:row^=piv[p]
   else:piv[p]=row;break
 free=[i for i in range(len(V)) if i not in piv];order=sorted(piv);Dbits=[1<<inds[x] for x in Dpts];projection={inds[x]:1<<i for i,x in enumerate(Dpts)};cb=[]
 for i in free:
  v=1<<i
  for p in order:
   if (piv[p]&v).bit_count()&1:v|=1<<p
  proj=0;tmp=v
  while tmp:
   l=tmp&-tmp;proj^=projection.get(l.bit_length()-1,0);tmp^=l
  cb.append((proj,v))
 qpiv={}
 def insert(v,src):
  while v:
   p=v.bit_length()-1
   if p in qpiv:v^=qpiv[p][0];src^=qpiv[p][1]
   else:qpiv[p]=(v,src);return(v,src)
  return None
 for b in base:
  src=0
  for i in range(192):
   if b>>i&1:src^=Dbits[i]
  assert insert(b,src) is not None
 glue=[]
 for proj,src in cb:
  ans=insert(proj,src)
  if ans:glue.append(ans)
 return glue,Dbits,len(free)
pvariants=[]
for r,s in itertools.combinations(range(6),2):
 loc=(((1<<32)-1)<<(32*r))|(((1<<32)-1)<<(32*s));old=bm([Dpts[i] for i in range(192) if loc>>i&1]);assert old.bit_count()==64;pvariants.append((loc,old))
