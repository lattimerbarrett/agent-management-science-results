from pathlib import Path
src=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
src=src.replace('N=12; g=25','N=11; g=23').replace('range(1,11)','range(1,15)').replace('(2*g-2 if n==0 else 1)','(48 if n==0 else 1)')
exec(src)
from sage.all import matrix,GF
import itertools,pickle,time
prime=1000000007;F=GF(prime);start=time.time()
@lru_cache(None)
def comps(d,n):
 if n==1:return ((d,),)
 return tuple((a,)+b for a in range(d+1) for b in comps(d-a,n-1))
@lru_cache(None)
def cols(d):return tuple((p,e) for k in range(d+1) for p in parts(k) for e in comps(d-k,4))
col11=cols(11);col10=cols(10);ix={x:i for i,x in enumerate(col11)}
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),-1,prime)%prime
rows=[]
for r in range(1,12):
 for avec in itertools.product(range(2),repeat=4):
  aa=sum(avec)
  for w in range(3*r-g-aa):
   if (r+w+aa)%2:continue
   for sig in parts(w):
    if any(v%3==2 for v in sig):continue
    rel={}
    for p,c in H(sig).items():
     d=r-sum(p)
     if d<0:continue
     for ev in comps(d,4):
      v=c
      for a,e in zip(avec,ev):v*= (A if a==0 else B)[e]
      if v:rel[(p,ev)]=mod(v)
    for q,fv in cols(11-r):
     rows.append({ix[(tuple(sorted(p+q)),tuple(e+f for e,f in zip(ev,fv)))]:v for (p,ev),v in rel.items()})
 print('r',r,'rows',len(rows),'time',time.time()-start,flush=True)
print('dims',len(rows),len(col11),'source',len(col10),flush=True)
R=matrix(F,len(rows),len(col11),{(i,j):v for i,row in enumerate(rows) for j,v in row.items()},sparse=False)
E=R.echelon_form();piv=E.pivots();free=[j for j in range(len(col11)) if j not in piv];E=E[:len(piv),:]
print('relationrank',len(piv),'quotient',len(free),'time',time.time()-start,flush=True)
pickle.dump((E,piv,free),open('workspace/agent4_k2cheap_checkpoint.pkl','wb'))
# Work in the much smaller relation space, imposing divisibility by psi1+psi2.
small=tuple((p,e) for k in range(12) for p in parts(k) for e in comps(11-k,3));smix={x:i for i,x in enumerate(small)}
projection=[(smix[(p,(e[0]+e[1],e[2],e[3]))],(-1)**e[1]) for p,e in col11]
T=matrix(F,E.nrows(),len(small))
for i,row in enumerate(E):
 tr=[F(0)]*len(small)
 for v,(j,sgn) in zip(row,projection):tr[j]+=sgn*v
 T[i]=tr
print('divisibility matrix',T.nrows(),T.ncols(),'time',time.time()-start,flush=True)
Z=T.left_kernel().basis_matrix();print('normal1 kernel',Z.nrows(),'time',time.time()-start,flush=True)
Div=Z*E;srcix={x:i for i,x in enumerate(col10)}
byb=[[j for j,(p,e) in enumerate(col11) if e[1]==b] for b in range(12)]
C=matrix(F,Div.nrows(),len(col10))
for i,row in enumerate(Div):
 rr=list(row);q=[F(0)]*len(col10)
 for b in range(11,0,-1):
  for j in byb[b]:
   v=rr[j]
   if not v:continue
   p,ev=col11[j];e=list(ev);e[1]-=1;q[srcix[(p,tuple(e))]]+=v
   e[0]+=1;rr[ix[(p,tuple(e))]]-=v;rr[j]=0
 assert not any(rr)
 C[i]=q
pickle.dump((C,E,piv,free),open('workspace/agent4_k2cheap_divided.pkl','wb'))
import json
lf=json.load(open('workspace/agent2_k2_functional25.json'));ld={(tuple(p),tuple(e)):v for (p,e),v in zip(lf['monomials'],lf['values'])}
lvec=matrix(F,len(col10),1,[ld[x] for x in col10]);vals=C*lvec
print('normal1 candidate pairings nonzero',sum(bool(v[0]) for v in vals),'of',C.nrows(),flush=True)
# Impose second normal by projection to the full relation quotient.
S=matrix(F,C.nrows(),len(col11))
for i,row in enumerate(C):
 for j,v in enumerate(row):
  if not v:continue
  p,e=col10[j]
  for z in (2,3):
   ev=list(e);ev[z]+=1;S[i,ix[(p,tuple(ev))]]+=v
Q=S.matrix_from_columns(free)-S.matrix_from_columns(piv)*E.matrix_from_columns(free)
K=Q.left_kernel().basis_matrix();Final=K*C
print('jointnormal kernel',Final.nrows(),'pairingsnonzero',sum(bool(v[0]) for v in Final*lvec),'time',time.time()-start,flush=True)
candidates=[[(col10[i][0],col10[i][1],int(v)) for i,v in enumerate(row) if v] for row in Final]
pickle.dump({'prime':prime,'columns10':col10,'c':candidates},open('workspace/agent4_k2cheap.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_k2cheap.py').write_text(Path(__file__).read_text())
