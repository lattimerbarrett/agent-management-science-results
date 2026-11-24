from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
import json
n=4;E=list(combinations(range(n),2));N=len(E);star=[{j for j,e in enumerate(E) if i in e} for i in range(n)]
def oldlift(P,i):return set(P)|{N+p*n+i for p in P}
def dummy(i):return {N+p*n+j for p in star[i] for j in range(n) if j!=i}
selected=[star[i]-{E.index(tuple(sorted((i,(i+1)%n))))} for i in range(n)]
support=[]
for i in range(n):support.extend([oldlift(selected[i],i),dummy(i)])
A=[[int(bool(p&q)) for q in support] for p in support];B=[[1-a for a in row] for row in A]
x=[F(1,2)]*(2*n);bonus=[F(i%2) for i in range(2*n)]
grad=[sum(B[i][j]*x[j] for j in range(2*n))+bonus[i] for i in range(2*n)]
def Q(v,AA=A,bon=bonus):
 return sum(v[i]*v[j]*(1-AA[i][j]) for i in range(len(v)) for j in range(i))+sum(a*b for a,b in zip(v,bon))
assert Q(x)==5
for i in range(n):assert grad[2*i]==grad[2*i+1]
G=[[A[2*i][2*j]-A[2*i][2*j+1]-A[2*i+1][2*j]+A[2*i+1][2*j+1] for j in range(n)] for i in range(n)]
assert G==[[2*int(i==j) for j in range(n)] for i in range(n)]
rows=[];eta=F(1,2);eps=eta/4
for owner in range(n):
 for size in [2,3]:
  for pp in combinations(star[owner],size):
   P=set(pp)
   if P==selected[owner]:continue
   new=oldlift(P,owner);an=[int(bool(new&S)) for S in support]
   gap=grad[2*owner]-sum((1-an[j])*x[j] for j in range(2*n))
   assert gap>=0
   a=[an[2*i]-an[2*i+1]-A[2*owner][2*i]+A[2*owner][2*i+1] for i in range(n)]
   norm=2-2*int(bool(new&support[2*owner]));energy=sum(v*v for v in a)
   assert energy<=16*gap/eta+4
   # Explicit globally feasible perturbation attaining the stated square completion.
   v=x+[eps];v[2*owner]-=eps
   for i in range(n):
    delta=-eps*F(a[i],2);v[2*i]+=delta;v[2*i+1]-=delta
   assert min(v)>=0 and all(v[2*i]+v[2*i+1]+(eps if i==owner else 0)==1 for i in range(n))
   AA=[row+[an[i]] for i,row in enumerate(A)]+[an+[1]]
   observed=Q(v,AA,bonus+[F(0)])-Q(x)
   predicted=-gap*eps+eps*eps*(F(energy,4)-F(norm,2))
   assert observed==predicted and observed<=0
   rows.append(dict(owner=owner,actual=sorted(P),gap=str(gap),energy=energy,norm=norm,objective_change=str(observed)))
print(json.dumps(dict(support_objective=str(Q(x)),root_gram=G,alternatives_checked=len(rows),details=rows),indent=2))
Path('workspace/agent1_orthogonal_gap_energy_check.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent1_orthogonal_gap_energy_check.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_orthogonal_gap_energy_lemma.txt').write_text('''ORTHOGONAL ROOT / NONSUPPORT GAP ENERGY LEMMA
LetQ be disjointness quadraticform(plusANYlinearbonus) oncolorprobabilitysimplexes,
A the0/1intersectionGram. Atglobalmaxx supposeeachcolorhasasupportedold/dummyroot
R_i=e_oldi-e_dummyi with <R_i,R_j>_A=2delta_ij andBOTHmasses>=eta>0.
Takeanynonsupportedalternativeofownerh, u=e_new-e_oldh. Letg=-DQ(x)[u]>=0,
a_i=<u,R_i>_A (so|a_i|<=2), and||u||_A^2 in{0,2}, assumingnonemptysets.
EveryrootdirectionhaszeroLINEARderivativebysupportedoptimality.
Setepsilon=eta/4,delta_i=-epsilon*a_i/2. Theperturbation
x+epsilon*u+sumdelta_i R_i isfeasible: everyold/dummymassmovesby<=epsilon,
exceptoldhwhichmovesby<=2epsilon, andallremainnonnegative; color sumsunchanged.
Sinceonzero-totalmassdirectionsB=J-A=-A, theobjectivechangeisEXACTLY
-g*epsilon +epsilon^2*(sum a_i^2/4 -||u||_A^2/2).
Globaloptimalitythereforeforces sum a_i^2<=16*g/eta+4.
Thusnon-supportalternativeshavefiniteEuclideanrootcorrelationenergycontrolledbytheir
first-ordergaps. NoHallboundhasbeenderivedfromthisyet.
CHECK: liftedduplicatecenter n4,m1,alpha1,w_i=1/2. Supportobjective5,rootGram2I;
ALL12alternativeoldpatterns(includingfull-staroldseeds)checkedwithexactFractions.
Explicitfeasibleperturbations/objectivechangesagreeidenticallywithsquare-completionformula.
''')
