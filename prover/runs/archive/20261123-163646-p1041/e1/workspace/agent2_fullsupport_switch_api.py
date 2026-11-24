"""Full weight-preserving coordinate-switch kernel for RM(7,14)."""
import pickle,numpy as np
cols=pickle.load(open('workspace/a1_cols13_degree5.pkl','rb'))
emb=[]
for p in range(14):
 t=np.arange(8192,dtype=np.uint16);emb.append((t&((1<<p)-1))|((t>>p)<<(p+1)))
def full_kernel(F,i):
 """Return (SS,K), where SS are derivative support points in compressed13
 coordinates; each K entry is a bitmask indexing SS, giving g in RM7,13.
 Every g supported on DiF is in the returned span. F XOR lift_i(g) has sameweight.
 """
 fb=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little')
 dx=fb[emb[i]]^fb[emb[i]^(1<<i)];SS=np.flatnonzero(dx).tolist();bas={};K=[]
 for j,x in enumerate(SS):
  v=cols[x];rel=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,rel);break
   a,b=bas[p];v^=a;rel^=b
  if not v:K.append(rel)
 return SS,K
def lift_rel(SS,rel,i):
 out=0
 while rel:
  bit=rel&-rel;x=SS[bit.bit_length()-1];a=int(emb[i][x]);out^=(1<<a)|(1<<(a^(1<<i)));rel^=bit
 return out

def full_kernel_direction(F,v):
 assert 0<v<16384
 i=(v&-v).bit_length()-1
 fb=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little')
 dx=fb[emb[i]]^fb[emb[i]^v];SS=np.flatnonzero(dx).tolist();bas={};K=[]
 for j,x in enumerate(SS):
  y=cols[x];rel=1<<j
  while y:
   p=y.bit_length()-1
   if p not in bas:bas[p]=(y,rel);break
   a,b=bas[p];y^=a;rel^=b
  if not y:K.append(rel)
 return SS,K
def lift_direction(SS,rel,v):
 i=(v&-v).bit_length()-1;out=0
 while rel:
  bit=rel&-rel;x=SS[bit.bit_length()-1];a=int(emb[i][x]);out^=(1<<a)|(1<<(a^v));rel^=bit
 return out
def direction_reps(masks):
 cells={}
 for i in range(14):
  membership=sum(((mask>>i)&1)<<j for j,mask in enumerate(masks))
  cells.setdefault(membership,i)
 ps=[0]
 for i in cells.values():ps +=[x^(1<<i) for x in ps]
 return ps[1:]
def quadratic_excess(SS,K):
 bas={}
 def ins(v):
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=v;return True
   v^=bas[p]
  return False
 L=[sum(((x>>i)&1)<<j for j,x in enumerate(SS)) for i in range(13)]
 ins((1<<len(SS))-1)
 for v in L:ins(v)
 for i in range(13):
  for j in range(i):ins(L[i]&L[j])
 excess=sum(ins(v) for v in K)
 return excess
