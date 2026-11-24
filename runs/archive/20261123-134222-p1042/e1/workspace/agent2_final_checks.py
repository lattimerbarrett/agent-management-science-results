import sys, itertools as it, math, json
from collections import defaultdict, Counter
sys.path.insert(0,'workspace')
from agent2_compute import make_complex,make_A,check,reduce_units
from sage.all import matrix,vector,QQ,ZZ

def base_check():
 cells,ds=make_complex(7);check(ds);active=None;units=[]
 for k in range(1,5):
  R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active)
  active=set(C);units.append(len(cells[k-1])-(len(R) if k==1 else len(R)))
  if k<4:assert not any(R.values())
 rows=list(R);cols=list(C);ci={j:i for i,j in enumerate(cols)}
 M=matrix(ZZ,len(rows),len(cols),{(i,ci[j]):v for i,r in enumerate(rows) for j,v in R[r].items()})
 S=M.smith_form(transformation=False);diag=[int(S[i,i]) for i in range(min(S.dimensions())) if S[i,i]]
 assert diag==[2] and M.nrows()==1 and M.ncols()==310
 return {'sizes':list(map(len,cells)),'residual_shape':list(M.dimensions()),'smith_nonzero':diag,'H3_free':0,'H4_free':309}

def core_check():
 cells,ds=make_A(4);d3=matrix(ZZ,len(cells[2]),len(cells[3]),ds[3]);d4=matrix(ZZ,len(cells[3]),len(cells[4]),ds[4]);vals=[]
 for f in cells[3]:
  missing=next(x for x in range(4) if x not in {x for x,y in f});cts=[sum(y==r for x,y in f) for r in range(3)];v=0
  if 2 in cts:
   r=cts.index(2);s=cts.index(1);v=1 if (r,s) in ((0,1),(1,2),(2,0)) else -1
  vals.append((-1)**missing*v)
 phi=vector(ZZ,vals);assert not any(phi*d4)
 K=d3.right_kernel_matrix();gg=math.gcd(*map(int,K*phi));assert gg==6
 # Compute actual augmented homology by unit cancellation in every degree.
 active=None;H=[]
 for k in range(1,7):
  R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active)
  assert not any(R.values());H.append(len(R));active=set(C)
 assert H==[0,0,0,1,2,0]
 return {'A4_augmented_sizes':list(map(len,cells)),'A4_reduced_H2_rank':1,'A4_reduced_H3_rank':2,'phi_gcd_on_full_integer_cycles':gg,'phi_kills_all_boundaries':True}

def add(P,Q):
 R=defaultdict(int,P)
 for m,c in Q.items():R[m]+=c
 return {m:c for m,c in R.items() if c}
def scale(P,c):return {m:c*v for m,v in P.items() if c*v}
def mult(P,Q):
 R=defaultdict(int)
 for a,c in P.items():
  for b,d in Q.items():
   if len({j for r,j in a+b})<len(a+b):continue
   R[tuple(sorted(a+b))]+=c*d
 return {m:c for m,c in R.items() if c}
def y(r,j):return {((r,j),):1}
def h(r,n):return {((r,j),):1 for j in range(n)}
def e2(r,n):return {((r,i),(r,j)):1 for i,j in it.combinations(range(n),2)}
def deriv(P):
 D=defaultdict(int)
 for m,c in P.items():
  for p,(r,j) in enumerate(m):D[(j,m[:p]+m[p+1:])]+=c
 return {m:c for m,c in D.items() if c}
def x_times(P,n):
 return {(j,m):c for m,c in P.items() for j in range(n) if j not in {jj for rr,jj in m}}
def fvalues(P):
 D=defaultdict(int)
 for m,c in P.items():
  cts=[sum(r==s for r,j in m) for s in range(3)]
  if 2 not in cts:continue
  r=cts.index(2);s=cts.index(1);sign=1 if (r,s) in ((0,1),(1,2),(2,0)) else -1
  D[tuple(sorted(j for r,j in m))]+=c*sign
 return D

def relation_checks(n):
 a,b=0,1;u=add(y(0,a),scale(y(1,a),-1));v=add(y(1,b),scale(y(2,b),-1))
 zs=mult(u,e2(2,n));ws=mult(u,h(2,n));zp=mult(mult(u,v),h(2,n));wp=mult(u,v)
 for z,w in ((zs,ws),(zp,wp)):
  assert all(sum(r==0 for r,j in m)<=1 and all(sum(r==s for r,j in m)<=2 for s in (1,2)) for m in z)
  assert deriv(z)==x_times(w,n)
 fs,fp=fvalues(zs),fvalues(zp)
 for T in it.combinations(range(n),3):
  assert fs.get(T,0)==(2 if a in T else 0)
  assert fp.get(T,0)==(-3 if a in T and b in T else 0)
 for S in it.combinations(range(n),4):
  assert sum(fs.get(T,0) for T in it.combinations(S,3))==6*(a in S)
  assert sum(fp.get(T,0) for T in it.combinations(S,3))==-6*(a in S and b in S)
 return {'n':n,'singleton_cycle_terms':len(zs),'pair_cycle_terms':len(zp),'all_dz_equals_xw_and_relation_coefficients_checked':True}

def local_core_checks():
 from agent2_anchor import make_A as make_A_b
 cases=[(3,(1,2,2),{2:2}),(2,(0,2,2),{1:1}),(2,(1,1,2),{1:2}),(1,(0,1,2),{0:1}),(1,(1,1,1),{0:2})]
 out=[]
 for q,b,expected in cases:
  cells,ds=make_A_b(q,b);active=None;hom={}
  for k in range(1,7):
   R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active)
   assert not any(R.values())
   if R:hom[k-2]=len(R)
   active=set(C)
  assert hom==expected,(q,b,hom,expected)
  out.append({'q':q,'caps':b,'sizes':list(map(len,cells)),'reduced_integral_homology_ranks':hom})
 return out

def run_checks():
 out={'base_m7':base_check(),'A4_functional':core_check(),'local_auxiliary_cores':local_core_checks(),'explicit_relations':[relation_checks(n) for n in range(6,13)]}
 print(json.dumps(out,indent=2))
 with open('workspace/agent2_final_checks.json','w') as f:json.dump(out,f,indent=2)
 return out
if __name__=='__main__':
 run_checks()
 with open('workspace/agent2_final_checks.py','w') as f:f.write(open(__file__).read())
