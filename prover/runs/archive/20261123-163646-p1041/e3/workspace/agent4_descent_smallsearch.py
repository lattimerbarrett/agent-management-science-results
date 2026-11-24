import numpy as np,itertools,time,json,pathlib
pathlib.Path('workspace/agent4_descent_smallsearch.py').write_text(pathlib.Path(__file__).read_text())
start=time.time();blocks=[]
for piv in itertools.combinations(range(8),4):
 free=[(i,j) for i,p in enumerate(piv) for j in range(p+1,8) if j not in piv]
 k=len(free);a=np.zeros((1<<k,4),dtype=np.uint8);a[:]=np.array([1<<p for p in piv],dtype=np.uint8)
 seq=np.arange(1<<k,dtype=np.uint32)
 for t,(i,j) in enumerate(free):a[:,i]^=(((seq>>t)&1)<<j).astype(np.uint8)
 blocks.append(a)
basis=np.concatenate(blocks);assert len(basis)==200787
spaces=np.zeros((len(basis),16),dtype=np.uint8)
for j in range(4):
 for k in range(1<<j):spaces[:,k|(1<<j)]=spaces[:,k]^basis[:,j]
print('built',time.time()-start,flush=True)
parity=np.array([i.bit_count()%2 for i in range(256)],dtype=np.uint8);xs=np.arange(256,dtype=np.uint8)
def fwht(a):
 a=a.copy();nn=a.shape[-1];sh=a.shape
 for j in range(nn.bit_length()-1):
  v=a.reshape(*sh[:-1],-1,2,1<<j);left=v[...,0,:].copy();right=v[...,1,:].copy();v[...,0,:]=left+right;v[...,1,:]=left-right
 return a
S=np.zeros(256,dtype=np.int16)
for x in range(256):
 q1=((x>>0)&1)*((x>>1)&1)^((x>>2)&1)*((x>>3)&1)
 q2=((x>>4)&1)*((x>>5)&1)^((x>>6)&1)*((x>>7)&1)
 S[x]=q1&q2
assert int(S.sum())==36
rng=np.random.default_rng(20260319);hist={};minslack=100;counter=None
for step in range(600):
 w=int(S.sum());wal=fwht(S);hits=fwht(wal[spaces]);assert np.all(hits%16==0);hits//=16;mx=int(hits.max());hist[(w,mx)]=hist.get((w,mx),0)+1;minslack=min(minslack,mx-8)
 if mx<=8:
  counter={'weight':w,'support':np.flatnonzero(S).tolist(),'max_flat_intersection':mx};break
 # random lowweight walk, avoid zero; prefer highweight to avoid spending all time minword
 newws=w+16-2*hits
 valid=(newws>=30)&(newws<=38)
 loc=np.flatnonzero(valid)
 if len(loc)==0:loc=np.flatnonzero((newws>=16)&(newws<=38))
 k=int(rng.choice(loc));row,k=divmod(k,16)
 char=np.array([(k>>j)&1 for j in range(4)],dtype=np.uint8)
 mask=np.all(parity[np.bitwise_and(basis[row,:,None],xs[None,:])]==char[:,None],axis=0)
 assert int(mask.sum())==16 and int(S[mask].sum())==int(hits[row,k]);S[mask]^=1
 if step%100==0:print(step,w,mx,time.time()-start,flush=True)
result={'steps':step+1,'counterexample':counter,'min_slack_above_half':minslack,'hist':{str(k):v for k,v in hist.items()},'seconds':time.time()-start}
pathlib.Path('workspace/agent4_descent_smallsearch.json').write_text(json.dumps(result,indent=2));print(result)
