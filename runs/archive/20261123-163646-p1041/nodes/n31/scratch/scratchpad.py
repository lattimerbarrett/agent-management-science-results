import numpy as np, random,time
rng=np.random.default_rng(721)
x=np.arange(128,dtype=np.uint16)
parity=np.array([v.bit_count()%2 for v in range(128)],dtype=np.uint16)
start=time.time();seen=set(); found=False
for batch in range(250):
 K=2048
 def mat_values(rank):
  masks=rng.integers(1,128,size=(K,rank),dtype=np.uint16)
  basis=rng.integers(1,128,size=(K,rank),dtype=np.uint16)
  return np.bitwise_xor.reduce(parity[masks[:,:,None]&x]*basis[:,:,None],axis=1)
 a=mat_values(random.choice([1,2,3,4]))^rng.integers(0,128,size=(K,1),dtype=np.uint16);b=mat_values(random.choice([1,2,3,4]))^rng.integers(0,128,size=(K,1),dtype=np.uint16)
 independent=(a!=0)&(a!=x)
 full=independent&(b!=0)&(b!=x)&(b!=a)&(b!=(a^x))
 t=full.sum(axis=1)
 seen.update(t.tolist())
 if np.any(t==33):
  i=np.flatnonzero(t==33)[0]; print('FOUND FANO rank3 count33',a[i].tolist(),b[i].tolist());found=True;break
print('elapsed',time.time()-start,'found',found,'small counts',sorted(v for v in seen if v<50))
