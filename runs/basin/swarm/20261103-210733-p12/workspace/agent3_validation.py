"""Independent exact Hodge checks and rational FZ reduction certificate."""
import sys,json,time
from pathlib import Path
from fractions import Fraction
from collections import Counter
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
import agent3_hodge as exact
import agent1_K as fast
from agent4_pairing import partitions
P=1000000007

def mod(x):
 q=Fraction(str(x));return q.numerator*pow(q.denominator,-1,P)%P

def validate_hodge():
 exact.validate();tests=0
 for g in range(2,9):
  ks=range(g+1) if g<=6 else [g-2]
  for k in ks:
   A=2*g-3-k
   if A<0:continue
   for aa in partitions(A):
    ds=tuple(a+1 for a in aa)
    value=sum(c*exact.F(g,ds,ms) for ms,c in exact.lambda_expansion(k))
    assert mod(value)==fast.J(g,k,ds),(g,k,ds,value)
    tests+=1
 print('Independent exact GRR-via-ch versus optimized Newton J:',tests,'checks')
 return tests

def certify_reduction():
 U=json.load(open('workspace/fz25_upper_data.json'));basis=list(map(tuple,U['basis']))
 M=sp.Matrix([[sp.Rational(x) for x in row] for row in U['matrix']])
 order=sorted(range(77),key=lambda i:(len(basis[i])+basis[i].count(1),basis[i]),reverse=True)
 R,piv=M[:,order].rref();assert len(piv)==33
 Edata=json.load(open('workspace/fz25_exceptional.json'));E0=[sp.Rational(0)]*77
 for a,c in zip(Edata['basis'],Edata['vector']):E0[basis.index(tuple(a))]=sp.Rational(c)
 P0=list(map(sp.Rational,json.load(open('workspace/agent2_Pgood.json'))['vector']))
 def reduce(v):
  v=[v[i] for i in order]
  for j,c in enumerate(piv):
   coeff=v[c]
   if coeff:v=[x-coeff*y for x,y in zip(v,R.row(j))]
  out=[None]*77
  for i,x in zip(order,v):out[i]=x
  return out
 Ep,Pp=reduce(E0),reduce(P0)
 saved=json.load(open('workspace/agent3_reduced_1.json'))
 assert [mod(x) for x in Ep]==saved['E']
 assert [mod(x) for x in Pp]==saved['P']
 psi=Counter()
 for i,x in enumerate(Pp):
  if not x:continue
  for j,y in enumerate(Ep):
   if not y:continue
   for a,c in exact.kappa_expansion(tuple(sorted(basis[i]+basis[j]))):
    psi[a]=(psi[a]+mod(x)*mod(y)*c)%P
 psi={a:c for a,c in psi.items() if c}
 assert psi=={tuple(a):c for a,c in saved['psi']}
 assert len(psi)==1042
 out={'basis':basis,'P':[str(x) for x in Pp],'E':[str(x) for x in Ep],
      'column_order':order,'pivot_columns_permuted':piv,
      'psi':[[a,c] for a,c in psi.items()]}
 json.dump(out,open('workspace/agent3_reduction_exact.json','w'))
 print('Exact rational FZ reductions verified; modular psi support',len(psi))

def assemble_scalar(recompute=False):
 data={}
 for f in Path('workspace').glob('*J*.json'):
  try:d=json.load(open(f))
  except Exception:continue
  if isinstance(d,dict) and all(k.isdigit() and isinstance(v,int) for k,v in d.items()):
   for k,v in d.items():
    if k in data:assert data[k]==v,(f,k)
    data[k]=v
 ps=list(partitions(24));idx={tuple(sorted(a)):i for i,a in enumerate(ps)}
 terms=json.load(open('workspace/agent3_reduced_1.json'))['psi']
 if recompute:
  import agent1_Kpersist as persistent
  cache='workspace/agent3_verify_roots_cache.pkl'
  if Path(cache).exists():persistent.load(cache)
  persistent.CACHE_FILE=cache
  for a,z in terms:
   i=idx[tuple(a)];value=persistent.J(25,23,tuple(x+1 for x in a))
   assert data[str(i)]==value,(i,a)
  persistent.save()
 bulk=sum(z*data[str(idx[tuple(a)])] for a,z in terms)%P
 assert bulk==250316045
 boundary=json.load(open('workspace/agent4_boundary_reduced1_scalar.json'))
 # Boundary is independently checked by agent4's exact-Q and Schur scripts.
 assert sum(boundary['contributions'])%P==boundary['scalar']==846247332
 total=(bulk+boundary['scalar'])%P
 assert total==96563370 and total!=0
 print('All1042bulk roots assembled:',bulk,'+ boundary846247332 =',total,'mod',P)
 return total

def original_psi_aggregate():
 U=json.load(open('workspace/fz25_upper_data.json'));basis=list(map(tuple,U['basis']))
 P0=[mod(x) for x in json.load(open('workspace/agent2_Pgood.json'))['vector']]
 d=json.load(open('workspace/fz25_exceptional.json'));E0=[0]*77
 for a,c in zip(d['basis'],d['vector']):E0[basis.index(tuple(a))]=mod(c)
 product=Counter()
 for a,x in zip(basis,P0):
  if x:
   for b,y in zip(basis,E0):
    if y:product[tuple(sorted(a+b))]=(product[tuple(sorted(a+b))]+x*y)%P
 psi=Counter()
 for a,z in product.items():
  if z:
   for pp,c in exact.kappa_expansion(a):psi[pp]=(psi[pp]+z*c)%P
 psi={a:z for a,z in psi.items() if z}
 assert len(psi)==1574
 json.dump([[a,z] for a,z in psi.items()],open('workspace/agent3_original_psi.json','w'))
 return psi

def assemble_original_scalar(recompute=False):
 psi=original_psi_aggregate();ps=list(partitions(24));idx={tuple(sorted(a)):i for i,a in enumerate(ps)};data={}
 for f in Path('workspace').glob('*J*.json'):
  try:d=json.load(open(f))
  except Exception:continue
  if isinstance(d,dict) and all(k.isdigit() and isinstance(v,int) for k,v in d.items()):
   for k,v in d.items():
    if k in data:assert data[k]==v,(f,k)
    data[k]=v
 if recompute:
  import agent1_Kpersist as persistent
  cache='workspace/agent3_verify_roots_cache.pkl'
  if Path(cache).exists():persistent.load(cache)
  persistent.CACHE_FILE=cache
  for a,z in psi.items():
   i=idx[a];assert data[str(i)]==persistent.J(25,23,tuple(x+1 for x in a))
  persistent.save()
 missing=[idx[a] for a in psi if str(idx[a]) not in data]
 assert not missing,missing
 bulk=sum(z*data[str(idx[a])] for a,z in psi.items())%P
 assert bulk==799683810,bulk
 d=json.load(open('workspace/agent4_boundary_good_actualQ.json'))
 # The boundary exact-Q driver checks its entries directly against rational support solutions.
 assert sum(d['split_contributions'])%P==d['scalar']==296879567
 total=(bulk+d['scalar'])%P
 assert total==96563370 and total!=0
 print('Original Pgood,E (no reduction lemma):',bulk,'+296879567=',total,'mod',P)
 return total

if __name__=='__main__':
 validate_hodge();assemble_original_scalar('--recompute-roots' in sys.argv)
