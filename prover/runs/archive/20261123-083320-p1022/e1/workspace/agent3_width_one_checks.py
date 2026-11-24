import sympy as s, random, json, os
from math import comb
rng=random.Random(3651)
n=2; d=5; N=d+2*n-1
mons=[(i,j,d-i-j) for i in range(d+1) for j in range(d+1-i)]
mons_next=[(i,j,d+1-i-j) for i in range(d+2) for j in range(d+2-i)]
idx={m:i for i,m in enumerate(mons_next)}
W=s.Matrix([[rng.randrange(-3,4) for _ in mons] for _ in range(N)])
M=s.zeros(len(mons_next),3*N)
for k in range(N):
 for var in range(3):
  for j,m in enumerate(mons):
   mm=list(m);mm[var]+=1
   M[idx[tuple(mm)],3*k+var]=W[k,j]
rank=M.rank()
assert rank==3*N
# Generic binary-support degree-d form variety in P(Sym^d C^{n+1})
# has dim = dim Gr(2,n+1) + d = 2(n-1)+d.
assert N>2*(n-1)+d
steiner_checks=[]
for nn in range(2,101):
 for a in range(2,101):
  ambient=a*(nn+1)
  rank2_dim=2*(a+nn-1)
  codim=ambient-rank2_dim
  assert codim==(a-2)*(nn-1)
  lower_rank=a*nn-codim
  assert lower_rank==a+2*nn-2>=2*nn
  steiner_checks.append([nn,a,lower_rank])
generalized_checks=[]
for nn in range(2,31):
 for a in range(1,21):
  for dd in range(1,21):
   if a*dd==1: continue
   # Generic S-valued binary degree-d forms have unique essential-variable plane.
   Xdim=2*nn-2+a*(dd+1)-1
   ambient=a*comb(nn+dd,dd)-1
   assert Xdim<=ambient
   Nmin=Xdim+1
   rmin=Nmin-a
   assert rmin==a*dd+2*nn-2>=2*nn
   generalized_checks.append([nn,a,dd,rmin])
out={'generalized_kernel_bound_checks':len(generalized_checks),'width_one_non_generated_example': {'n':n,'d':d,'N':N,'rank_E':N-1,'h0_E':3*N-rank,'multiplication_rank':rank,'matrix_rows':M.rows,'matrix_cols':M.cols,'W_coefficients':W.tolist(),'monomials':mons}, 'steiner_bound_checks':len(steiner_checks)}
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_width_one_checks.json','w') as f: json.dump(out,f,default=int)
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_width_one_checks.py'):
 source=open(__file__).read()
 with open('workspace/agent3_width_one_checks.py','w') as f:
  f.write(source)
print(json.dumps({k:v for k,v in out.items() if k!='width_one_non_generated_example'}))
print('Exact multiplication matrix rank',rank,'of',M.rows,'by',M.cols,'so generic kernel bundle has h0=0.')
