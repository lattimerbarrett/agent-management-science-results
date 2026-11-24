from pathlib import Path
source=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
source=source.replace('N=12; g=25','N=13; g=24').replace('range(1,11)','range(1,15)').replace('(2*g-2 if n==0 else 1)','(2*g if n==0 else 1)')
exec(source)
from sage.all import matrix,GF
import time,pickle,itertools
start=time.time();prime=1000000007;F=GF(prime)
def cols_at(d):return [(p,a,d-sum(p)-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
cols13=cols_at(13);ix={p:i for i,p in enumerate(cols13)};cols12=cols_at(12)
print('columns',len(cols13),len(cols12),flush=True)
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),-1,prime)%prime
rows=[]
for r in range(1,14):
 for a1,a2 in itertools.product(range(2),repeat=2):
  for weight in range(3*r-g-a1-a2):
   if (r+weight+a1+a2)%2!=1:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    rel={}
    for p,x in H(sig).items():
     k=sum(p)
     if k>r:continue
     for e1 in range(r-k+1):
      e2=r-k-e1;y=x*(A if a1==0 else B)[e1]*(A if a2==0 else B)[e2]
      if y:rel[(p,e1,e2)]=mod(y)
    for q,b1,b2 in cols_at(13-r):
     row={ix[(tuple(sorted(p+q)),e1+b1,e2+b2)]:x for (p,e1,e2),x in rel.items()}
     rows.append(row)
 print('r',r,'rows',len(rows),'elapsed',time.time()-start,flush=True)
R=matrix(F,len(rows),len(cols13),{(i,j):v for i,row in enumerate(rows) for j,v in row.items()},sparse=False)
print('matrix constructed',time.time()-start,flush=True)
E=R.echelon_form();piv=E.pivots();free=[j for j in range(len(cols13)) if j not in piv];E=E[:len(piv),:]
print('rank',len(piv),'qdim',len(free),'elapsed',time.time()-start,flush=True)
# Matrix of multiplication ψ1+ψ2 modulo relations.
C=matrix(F,len(cols12),len(free));freeix={j:k for k,j in enumerate(free)};pivix={j:k for k,j in enumerate(piv)}
for i,(p,a,b) in enumerate(cols12):
 row=F**len(cols13)
 v=row(0);v[ix[(p,a+1,b)]]=1;v[ix[(p,a,b+1)]]=1
 # pivots eliminated by subtracting pivot rows
 for j in piv:
  if v[j]:v-=v[j]*E[pivix[j]]
 C[i]=[v[j] for j in free]
# b must have at least one ψ exponent.
keep=[i for i,(p,a,b) in enumerate(cols12) if a+b]
K=C[keep,:].left_kernel().basis_matrix()
print('annihilator dim',K.nrows(),'elapsed',time.time()-start,flush=True)
bs=[]
for row in K:
 bs.append([(cols12[i][0],cols12[i][1],cols12[i][2],int(x)) for i,x in zip(keep,row) if x])
pickle.dump({'prime':prime,'columns12':cols12,'columns13':cols13,'b':bs},open('workspace/agent3_pointed_boundary_test.pkl','wb'))
Path('workspace/agent3_pointed_boundary_test.py').write_text(Path(__file__).read_text())
