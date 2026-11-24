import pickle,numpy as np,json,itertools
OP0=pickle.load(open('old_min_tensor_profiles.pkl','rb'));NP=pickle.load(open('experiments/e1/agent3_exact_8_14_16_profiles.pkl','rb'))['profiles'];OP={}
def profile(F):
 return tuple((sumxor(F,u)).bit_count() for u in range(1,8))
def sumxor(F,u):
 v=0
 for i,f in enumerate(F):
  if u>>i&1:v^=f
 return v
for F in OP0.values():
 for u in [1,2,3]:
  for v in [1,2,3]:
   if u==v:continue
   for w in [4,5,6,7]:
    G=tuple(sumxor(F,t) for t in [u,v,w]);OP[profile(G)]=G
print('old mixed profiles',len(OP))
newkeys=list(NP);oldkeys=list(OP)
cnt=np.array([[-sum((-1 if (u&b).bit_count()%2 else 1)*pr[u-1] for u in range(1,8))//4 for b in range(1,8)] for pr in newkeys],dtype=np.int64)
W=np.array(oldkeys,dtype=np.int64)@cnt.T
found={}
for target in [310,322,326,330,334]:
 hits=np.argwhere(W==target);print('target',target,'profilepairs',len(hits),flush=True)
 if len(hits):
  i,j=hits[0];fs=OP[oldkeys[i]];gs=NP[newkeys[j]]
  vals=np.array([sum(((f>>x)&1)*((g>>y)&1) for f,g in zip(fs,gs))%2 for y in range(128) for x in range(128)],dtype=np.uint8)
  anf=vals.copy()
  for bit in range(14):
   st=1<<bit
   for off in range(0,16384,2*st):anf[off+st:off+2*st]^=anf[off:off+st]
  degree=max((x.bit_count() for x in np.flatnonzero(anf).tolist()),default=-1)
  print('VERIFIED',int(vals.sum()),degree)
  found[target]={'old':list(map(hex,fs)),'new':list(map(hex,gs)),'degree':degree}
json.dump(found,open('mixed_tensor_target_witnesses.json','w'))