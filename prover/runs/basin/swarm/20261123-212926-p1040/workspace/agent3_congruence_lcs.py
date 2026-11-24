from pathlib import Path
import numpy as np,time,json

def setup(m,k):
 M=2**k;I=tuple(int(i==j) for i in range(m) for j in range(m));eye=np.eye(m,dtype=np.int64)
 def mul(A,B):return tuple(map(int,((np.array(A,dtype=np.int64).reshape(m,m)@np.array(B,dtype=np.int64).reshape(m,m))%M).flat))
 def inv(A):
  B=(np.array(A,dtype=np.int64).reshape(m,m)-eye)%M
  out=eye.copy();term=eye.copy()
  for j in range(1,k):term=(-term@B)%M;out=(out+term)%M
  return tuple(map(int,out.flat))
 def comm(A,B):return mul(mul(mul(A,B),inv(A)),inv(B))
 def lead(A):
  ds=[(v-int(i==j))%M for i in range(m) for j,v in enumerate(A[i*m:(i+1)*m])]
  vals=[((d&-d).bit_length()-1,t) for t,d in enumerate(ds) if d]
  return min(vals) if vals else None
 gs=[]
 for i in range(m):
  a=list(I);a[i*m+i]=M-1;gs.append(tuple(a))
  for j in range(m):
   if i!=j:a=list(I);a[i*m+j]=2;gs.append(tuple(a))
 def reduce(A,piv):
  while A!=I:
   key=lead(A)
   if key not in piv:return A
   A=mul(A,inv(piv[key]))
  return A
 def subgroup(seeds,normal=False):
  piv={};q=list(seeds)
  while q:
   A=reduce(q.pop(),piv)
   if A==I:continue
   key=lead(A)
   old=list(piv.values());piv[key]=A
   q.append(mul(A,A))
   q.extend(comm(A,B) for B in old)
   if normal:q.extend(comm(A,g) for g in gs)
  # Full closed-polycyclic certificate.
  bs=list(piv.values())
  assert all(reduce(mul(a,a),piv)==I for a in bs)
  assert all(reduce(comm(a,b),piv)==I for a in bs for b in bs)
  assert all(reduce(a,piv)==I for a in seeds)
  if normal:assert all(reduce(comm(a,g),piv)==I for a in bs for g in gs)
  return piv
 G=subgroup(gs);layers=[G];H=G
 for r in range(2,5):
  H=subgroup([comm(h,g) for h in H.values() for g in gs],True);layers.append(H)
 U=list(I);U[1]=-2%M;U=tuple(U)
 V=list(I);V[m]=2;V=tuple(V)
 D=list(I);D[0]=M-1;D=tuple(D)
 W=comm(comm(V,U),D)
 member=reduce(W,H)==I
 return {'m':m,'modulus':M,'log2_layer_orders':[len(L) for L in layers],'W_in_gamma4':member,'W_identity':W==I}
if __name__=='__main__':
 results=[]
 for m in [2,3,4]:
  for k in [4,5,6,8]:
   t=time.time();res=setup(m,k);res['seconds']=time.time()-t;results.append(res);print(res,flush=True)
 Path('workspace/agent3_congruence_lcs_results.json').write_text(json.dumps(results))
