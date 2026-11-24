import itertools,json,numpy as np,time
from pathlib import Path
from scipy.optimize import linprog
from z3 import Solver,Bool,Or,PbLe,unsat
base_json=json.load(open('workspace/agent3_fano_pruning_checks.json'))
H=[tuple(E) for Fi in base_json['classes'] for E in Fi]
U={3,4,5,6}
E=[]
for A in H:
 for inners in itertools.product(H,repeat=3):
  E.append(frozenset(7*a+b for a,B in zip(A,inners) for b in B))
assert len(E)==1296 and len(set(E))==1296 and all(len(F)==9 for F in E)
assert all(A&B for A,B in itertools.combinations(E,2))
M=np.zeros((len(E),49))
for i,A in enumerate(E):M[i,list(A)]=1
res=linprog(np.ones(49),A_ub=-M,b_ub=-np.ones(len(E)),bounds=(0,None),method='highs')
cap=linprog(np.ones(49),A_ub=-M,b_ub=-np.ones(len(E)),bounds=(0,1/8),method='highs')
assert res.success and abs(res.fun-4)<1e-8
assert cap.success and cap.fun>4+1e-6
x=np.array([.25 if a in U and b in U else 0 for a in range(7) for b in range(7)])
assert np.all(M@x==1) and x.sum()==4
loads=M.sum(axis=0)/324
assert loads.max()==1 and abs(len(E)/324-4)<1e-10
assert all((loads[7*a+b]==1)==(a in U and b in U) for a in range(7) for b in range(7))
vs=[Bool('c%d'%i) for i in range(49)];s=Solver();s.set(timeout=60000)
for A in E:s.add(Or([vs[v] for v in A]))
s.add(PbLe([(v,1) for v in vs],8));t=time.time();ans=s.check()
assert ans==unsat
cover9={7*a+b for a in range(3) for b in range(3)}
assert all(F&cover9 for F in E)
R=dict(edges=len(E),vertices=49,rank=9,cover_number=9,fractional_cover=float(res.fun),capped_fractional_cover=float(cap.fun),cap=1/8,eight_cover_solver=str(ans),solver_seconds=time.time()-t,optimal_positive_points=[i for i,w in enumerate(x) if w>0],fractional_matching_weight_each='1/324')
Path('workspace/agent3_capped_cover_tensor_counter.json').write_text(json.dumps(R,indent=2));print(json.dumps(R,indent=2))
Path('workspace/agent3_capped_cover_tensor_counter.py').write_text(Path('scratchpad.py').read_text())