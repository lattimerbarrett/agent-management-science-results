from rank4_finite_helpers import *
from scipy.sparse import kron,eye,save_npz,load_npz
from pathlib import Path
import sys
sys.path.insert(0,'experiments/e1')
from agent3_cvec_basis import CVecBasis
T0=time.time();cache=Path('rank4_d7');cache.mkdir(exist_ok=True)
ops={a:build(g) for a,g in G.items()}
print('scalar ops ready',time.time()-T0,flush=True)
# All displacements of minimum degree four, output-major.
hi=[j for j,w in enumerate(words) if len(w)>=4];hw=[words[j] for j in hi];hx={w:j for j,w in enumerate(hw)};mh=len(hw)
def ad_matrix(g):
 path=cache/f'N{g}.npz'
 if path.exists():return load_npz(path)
 rr=[];cc=[];vv=[]
 for i in range(N):
  p=ops[g][:,i].tocoo()
  for row,coef in zip(p.row,p.data):
   v=words[row]
   if len(v)>4:continue
   for pos,j in enumerate(v):
    for w in hw:
     if len(v)+len(w)>D+1:break
     u=v[:pos]+w+v[pos+1:]
     rr.append(i*mh+hx[u]);cc.append(j*mh+hx[w]);vv.append(int(coef))
 J=coo_matrix((np.array(vv,dtype=np.int32),(rr,cc)),shape=(N*mh,N*mh)).tocsr()
 A=kron(eye(N,dtype=np.int32),ops[-g][hi,:][:,hi],format='csr')@J-eye(N*mh,dtype=np.int32)
 A=A.tocsr();A.data%=3;A.eliminate_zeros();A.data=A.data.astype(np.int16)
 save_npz(path,A);return A
Ns=[ad_matrix(g) for g in range(1,25)]
print('adjoints ready',time.time()-T0,flush=True)
def inds(lo,up):return np.array([i*mh+j for i in range(N) for j,w in enumerate(hw) if lo<=len(w)<=up])
def coord(lo,up):
 ws=[w for w in hw if lo<=len(w)<=up];m=len(ws)
 return np.array([i*m+j for i in range(N) for j,w in enumerate(ws) if all(w<w[k:]+w[:k] for k in range(1,len(w)))])
def maps(lo,up,lo2,up2):
 ii=inds(lo,up);oo=inds(lo2,up2)
 return [A[oo,:][:,ii].tocsr() for A in Ns]
def inv(w):return tuple(-a for a in reversed(w))
def comm(u,v):return u+v+inv(u)+inv(v)
small=sum(N**d for d in range(1,6));ops5={g:S[:small,:small] for g,S in ops.items()}
E=np.zeros((small,N),dtype=np.int16);E[:N]=np.eye(N,dtype=np.int16)
s4=sum(N**d for d in range(1,4))
def ev(w,ops,E):
 V=E.copy()
 for a in reversed(w):V=(ops[a]@V)%3
 return (V-E)%3

def stage3():
 fn=cache/'B3.npy'
 if fn.exists():return np.load(fn)
 c=coord(4,5);B=CVecBasis(len(c));raw=[]
 for a,b,k in product(range(1,25),repeat=3):
  if a==b:continue
  V=ev(comm(comm((a,),(b,)),(k,)),ops5,E)
  assert not V[:s4].any()
  row=V[s4:].T.reshape(-1).astype(np.uint8)
  if B.insert(row[c]):raw.append(row)
 print('triple seed rank',len(raw),time.time()-T0,flush=True)
 mm=maps(4,5,4,5);old=np.array(raw,dtype=np.uint8)
 for g,A in enumerate(mm):
  for j in range(0,len(old),64):
   rows=((A@old[j:j+64].T).T%3).astype(np.uint8)
   for row in rows:
    if B.insert(row[c]):raw.append(row)
 print('normal triple span',len(raw),time.time()-T0,flush=True)
 # Further images of the new rows vanish: they have minimum degree five.
 out=np.array(raw,dtype=np.uint8);np.save(fn,out);return out
B3=stage3()
def build_stage(Bin,lo,up,lo2,up2,name,save_full=True):
 fn=cache/(name+'.npy')
 if fn.exists():return np.load(fn)
 c=coord(lo2,up2);B=CVecBasis(len(c));raw=[]
 mm=maps(lo,up,lo2,up2)
 for g,A in enumerate(mm):
  for j in range(0,len(Bin),48):
   rows=((A@Bin[j:j+48].T).T%3).astype(np.uint8)
   for row in rows:
    if B.insert(row[c]):raw.append(row)
  print(name,'generator',g,'rank',len(raw),'seconds',time.time()-T0,flush=True)
 # Close under conjugation; one iteration suffices on this two-degree window.
 old=np.array(raw,dtype=np.uint8);mm=maps(lo2,up2,lo2,up2)
 for g,A in enumerate(mm):
  for j in range(0,len(old),48):
   rows=((A@old[j:j+48].T).T%3).astype(np.uint8)
   for row in rows:
    if B.insert(row[c]):raw.append(row)
  print(name,'normal',g,'rank',len(raw),'seconds',time.time()-T0,flush=True)
 out=np.array(raw,dtype=np.uint8);np.save(fn,out);return out
B4=build_stage(B3,4,5,5,6,'B4')
# Gamma5 output is degrees6 and7. Retain only leading degree6 for normal closure,
# and full selected coordinates for final rowspace testing.
c5=coord(6,7);B=CVecBasis(len(c5));leading=[]
outws=[w for w in hw if 6<=len(w)<=7];mout=len(outws)
leadidx=np.array([i*mout+j for i in range(N) for j,w in enumerate(outws) if len(w)==6])
mm=maps(5,6,6,7)
for g,A in enumerate(mm):
 for j in range(0,len(B4),32):
  rows=((A@B4[j:j+32].T).T%3).astype(np.uint8)
  for row in rows:
   if B.insert(row[c5]):leading.append(row[leadidx])
 print('B5 generator',g,'rank',len(leading),'seconds',time.time()-T0,flush=True)
# Only degree6 is needed when applying one more conjugation difference.
lead=np.array(leading,dtype=np.uint8);r0=len(lead);mm=maps(6,6,6,7)
for g,A in enumerate(mm):
 for j in range(0,len(lead),32):
  rows=((A@lead[j:j+32].T).T%3).astype(np.uint8)
  for row in rows:
   if B.insert(row[c5]):leading.append(row[leadidx])
 print('B5 normal',g,'rank',len(leading),'seconds',time.time()-T0,flush=True)
# Original rank3 word, extended by fixing x4.
lookup={name:i+1 for i,name in enumerate(names)}
g0=lookup['K',0,1];g1=lookup['K',0,2];g3=lookup['K',1,0];g4=lookup['K',1,2];g7=lookup['K',2,1];g8=lookup['C',2,0,1]
def TT(a,b,c,d):return comm(comm(comm((a,),(b,)),(c,)),(-d,))
W=TT(g0,g8,g3,g1)+TT(g0,g8,g3,g4)+TT(g4,g3,g8,g0)+inv(TT(g4,g7,g8,g3))
EE=np.zeros((M,N),dtype=np.int16);EE[:N]=np.eye(N,dtype=np.int16)
V=ev(W,ops,EE)
assert not V[:sum(N**d for d in range(1,6))].any()
row=V[sum(N**d for d in range(1,6)):].T.reshape(-1)
r=B.info()[0];outside=B.insert(row[c5])
print('RESULT gamma5 rank',r,'W outside?',outside,'elapsed',time.time()-T0,flush=True)
import json
json.dump({'rank':int(r),'outside':bool(outside),'seconds':time.time()-T0},open(cache/'result.json','w'))
