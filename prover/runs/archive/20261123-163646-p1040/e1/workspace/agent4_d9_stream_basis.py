import sys,os,json,time
from pathlib import Path
import numpy as np
from scipy.sparse import load_npz
from sage.all import libgap
libgap.eval('LoadPackage("cvec",false:OnlyNeeded:=true)');libgap.eval('LoadPackage("io",false:OnlyNeeded:=true)')
CLEANWRITE=libgap.eval('function(B,v,f)local r,s;r:=CleanRow(B,v,true,fail);if r=false then s:="";CVEC_CVEC_TO_EXTREP(v,s);IO_Write(f,s);IO_Flush(f);return true;fi;return false;end')
ESCAPES=['\\%03o'%b for b in range(256)]
class StreamBasis:
 def __init__(self,n,path,perm=None,lowmask=None):
  self.n=n;self.perm=np.arange(n) if perm is None else perm;self.iperm=np.argsort(self.perm)
  self.lowmask=lowmask;self.cl=libgap.CVecClass(3,1,n);self.basis=libgap.EmptySemiEchelonBasis(libgap.CMat([],self.cl))
  self.file=libgap.IO_File(path,'w');self.fd=os.open(path,os.O_RDONLY);self.offset=0;self.nb=((n+9)//10)*4;self.rank=0;self.active=[]
 def insert(self,row):
  a=np.asarray(row,dtype=np.uint32)[self.perm]%3
  if not a.any():return False
  a=np.pad(a,(0,(-len(a))%10));raw=(a.reshape(-1,10)<<np.arange(0,30,3,dtype=np.uint32)).sum(axis=1,dtype=np.uint32).astype('<u4').tobytes()
  s=libgap.eval('"'+''.join(ESCAPES[b] for b in raw)+'"');v=libgap.CVec(self.cl);libgap.CVEC_EXTREP_TO_CVEC(s,v)
  if not bool(CLEANWRITE(self.basis,v,self.file)):return False
  raw=os.pread(self.fd,self.nb,self.offset);assert len(raw)==self.nb,(len(raw),self.nb)
  self.offset+=self.nb;self.rank+=1
  raw=np.frombuffer(raw,dtype='<u4');out=((raw[:,None]>>np.arange(0,30,3,dtype=np.uint32))&7).astype(np.uint8).ravel()[:self.n][self.iperm]
  assert np.all(out<3)
  if self.lowmask is None or out[self.lowmask].any():self.active.append(out)
  return True
 def finish(self,prefix):
  libgap.IO_Close(self.file);os.close(self.fd)
  np.save(prefix+'_active.npy',np.array(self.active,dtype=np.uint8))
  Path(prefix+'_meta.json').write_text(json.dumps({'rank':self.rank,'active':len(self.active),'n':self.n,'record_bytes':self.nb,'packed_file':prefix+'_basis.packed'}))

# Independent exact small test of residual serialization and rank.
from sage.all import matrix,GF
rng=np.random.default_rng(123);T=rng.integers(0,3,(120,200),dtype=np.uint8);T[80:]=T[:40]
B=StreamBasis(200,'workspace/agent4_cvec_test.packed')
for row in T:B.insert(row)
assert B.rank==matrix(GF(3),T.tolist()).rank()==80
assert matrix(GF(3),np.array(B.active).tolist()).rank()==80
B.finish('workspace/agent4_cvec_test')
print('PASS streamingCVECresidualrank80',flush=True)

LO=5;D=9;M=sum(3**d for d in range(LO,D+1));N=3*M
starts={d:sum(3**k for k in range(LO,d)) for d in range(LO,D+2)}
perm=np.concatenate([np.arange(i*M+starts[d],i*M+starts[d+1]) for d in range(LO,D+1) for i in range(3)])
lowmask=np.concatenate([np.arange(i*M,i*M+starts[9]) for i in range(3)])
M4=M+81;keep=np.concatenate([np.arange(i*M4+81,(i+1)*M4) for i in range(3)])
Ops=[load_npz(f'workspace/agent4_tensor_d9_N_{g}.npz')[keep,:][:,keep].tocsr() for g in range(9)]
t=time.time();prefix='workspace/agent4_d9_L4';B=StreamBasis(N,prefix+'_basis.packed',perm,lowmask)
for g in range(9):
 seeds=np.load(f'workspace/agent4_gamma4_d9_log_seeds_{g}.npz')['seeds'].reshape(729,N)
 for row in seeds:B.insert(row)
 print('initialg',g,'rank',B.rank,'active',len(B.active),'seconds',round(time.time()-t,1),flush=True)
# Full normalclosure: everynewnoncentral-degree residual is queued once.
j=0
while j<len(B.active):
 end=min(j+32,len(B.active));A=np.array(B.active[j:end],dtype=np.uint8)
 for k,Op in enumerate(Ops):
  images=(Op@A.T).T%3
  for row in images:B.insert(row)
 j=end
 if j%256==0 or j==len(B.active):print('closure processed',j,'/',len(B.active),'rank',B.rank,'seconds',round(time.time()-t,1),flush=True)
B.finish(prefix)
print('FINAL L4rank',B.rank,'active',len(B.active),'seconds',time.time()-t,flush=True)
