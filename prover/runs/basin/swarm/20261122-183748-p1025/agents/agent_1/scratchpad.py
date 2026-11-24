from z3 import *
import itertools,time,collections,json
set_param(proof=True)
V=list(itertools.combinations(range(7),3));n=len(V)
orders=[
[9,10,12,18,31,0,3,7,17,32,4,8,11,13,14,16,33,24,25,2,23,26,6,34,15,22,5,1,27,28,30,19,20,29,21],
[12,15,18,21,27,13,17,20,26,14,16,19,25,2,4,23,3,22,30,33,24,10,11,6,9,0,29,32,8,1,7,31,28,5,34],
[4,25,26,28,31,3,27,29,32,5,7,10,23,16,18,19,21,11,17,22,8,2,12,13,20,14,30,1,24,9,6,0,33,15,34]]
assert all(sorted(order)==list(range(n)) for order in orders)
positions=[{v:i for i,v in enumerate(order)} for order in orders]
boxes=[[(p[i],max(p[j] for j in range(n) if i==j or not set(V[i])&set(V[j]))) for p in positions] for i in range(n)]
for i in range(n):
 for j in range(i):
  overlap=all(max(boxes[i][k][0],boxes[j][k][0])<=min(boxes[i][k][1],boxes[j][k][1]) for k in range(3))
  assert overlap == (not set(V[i])&set(V[j]))
print('Upper bound checked')
# order q[k,i,j] signifies left i < left j; use signs
q={};var={};clauses=[]
def new(name):
 i=len(var)+1;var[i]=Bool(name);return i
for k in range(2):
 for i in range(n):
  for j in range(i):q[k,i,j]=new(f'o{k}_{i}_{j}');q[k,j,i]=-q[k,i,j]
def add(*xs):
 c=set(xs)
 if any(-x in c for x in c):return
 clauses.append(tuple(sorted(c)))
for k in range(2):
 for a,b,c in itertools.combinations(range(n),3):
  add(-q[k,a,b],-q[k,b,c],q[k,a,c]);add(q[k,a,b],q[k,b,c],-q[k,a,c])
N=[[j for j in range(n) if i==j or not set(V[i])&set(V[j])] for i in range(n)]
sep={}
for i in range(n):
 for j in range(i):
  if j in N[i]:continue
  choices=[]
  for k in range(2):
   for a,b in ((i,j),(j,i)):
    x=new(f's{k}_{a}_{b}');sep[k,a,b]=x;choices.append(x)
    for z in N[a]:add(-x,q[k,z,b])
  add(*choices)
add(sep[0,0,1])
print('vars clauses',len(var),len(clauses),flush=True)
s=Solver();s.set(auto_config=False)
for c in clauses:s.add(Or([var[x] if x>0 else Not(var[-x]) for x in c]))
t=time.time();result=s.check();assert result==unsat
print(result,time.time()-t,flush=True)
p=s.proof()
# Independent propositional proof checker. Dependencies are sets of
# temporary hypotheses, encoded as integer bitsets.
ids={v.get_id():i for i,v in var.items()}
from functools import lru_cache
@lru_cache(None)
def lit(e):
 if is_not(e):return -lit(e.arg(0))
 assert e.get_id() in ids
 return ids[e.get_id()]
@lru_cache(None)
def clause(e):
 if is_false(e):return frozenset()
 if is_or(e):return frozenset(lit(c) for c in e.children())
 return frozenset([lit(e)])
initial=set(map(frozenset,clauses))
hypbits={}
def hbit(l):
 if l not in hypbits:hypbits[l]=1<<len(hypbits)
 return hypbits[l]
# Truth table evaluator using bitsets: one bit per assignment.
def tautological_inference(premises,conclusion):
 atoms={};todo=list(premises)+[conclusion];seen=set()
 while todo:
  e=todo.pop()
  if e.get_id() in seen:continue
  seen.add(e.get_id())
  if e.get_id() in ids:atoms[e.get_id()]=len(atoms)
  else:todo.extend(e.children())
 assert len(atoms)<=12
 rows=1<<len(atoms);mask=(1<<rows)-1
 values={i:sum(1<<r for r in range(rows) if r>>j&1) for i,j in atoms.items()}
 def ev(e):
  i=e.get_id()
  if i in values:return values[i]
  if is_true(e):v=mask
  elif is_false(e):v=0
  elif is_not(e):v=mask^ev(e.arg(0))
  elif is_or(e):
   v=0
   for c in e.children():v|=ev(c)
  elif is_and(e):
   v=mask
   for c in e.children():v&=ev(c)
  elif is_eq(e):v=mask^(ev(e.arg(0))^ev(e.arg(1)))
  elif is_implies(e):v=(mask^ev(e.arg(0)))|ev(e.arg(1))
  else:raise AssertionError(e)
  values[i]=v;return v
 antecedent=mask
 for e in premises:antecedent&=ev(e)
 assert antecedent & (mask^ev(conclusion))==0
checked={};stack=[(p,False)];counts=collections.Counter()
t=time.time()
while stack:
 node,ready=stack.pop();idx=node.get_id()
 if idx in checked:continue
 children=node.children();prem=children[:-1];con=children[-1]
 if not ready:
  stack.append((node,True))
  stack.extend((c,False) for c in prem if c.get_id() not in checked)
  continue
 name=str(node.decl());counts[name]+=1
 dep=0
 for c in prem:dep|=checked[c.get_id()]
 if name=='asserted':
  assert not prem and clause(con) in initial
 elif name=='hypothesis':
  assert not prem;dep=hbit(lit(con))
 elif name=='lemma':
  assert len(prem)==1 and is_false(prem[0].arg(prem[0].num_args()-1))
  for l in clause(con):dep &= ~hypbits.get(-l,0)
 elif name=='unit-resolution':
  cs=[clause(c.arg(c.num_args()-1)) for c in prem]
  residual=set(cs[0])
  for unit in cs[1:]:
   assert len(unit)==1
   l=next(iter(unit));assert -l in residual
   residual.remove(-l)
  assert frozenset(residual)==clause(con)
 else:
  # No trust in the named rule: check its local propositional truth table.
  tautological_inference([c.arg(c.num_args()-1) for c in prem],con)
 checked[idx]=dep
assert is_false(p.arg(p.num_args()-1)) and checked[p.get_id()]==0
print('VERIFIED',len(checked),'proof steps',dict(counts),'time',time.time()-t,flush=True)

