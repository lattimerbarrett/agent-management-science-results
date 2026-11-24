import sympy as s,itertools,json,os
from pathlib import Path
J=s.zeros(6)
for i in [0,2,4]: J[i,i+1]=1;J[i+1,i]=-1
assert J.det()==1 and J.rank()==6
results=[]
for piv in itertools.combinations(range(6),4):
 M=s.zeros(6,4)
 for j,i in enumerate(piv): M[i,j]=1
 free=[i for i in range(6) if i not in piv]
 vv=s.symbols('x0:8')
 for z,(i,j) in enumerate(itertools.product(free,range(4))): M[i,j]=vv[z]
 F=M.T*J*M
 equations=[F[i,j] for i in range(4) for j in range(i+1,4)]
 G=s.groebner(equations,*vv)
 assert list(G)==[s.Integer(1)]
 results.append({'pivot_rows':piv,'groebner_basis':['1']})
 print(piv,'verified no isotropic 4-plane',flush=True)
omega=s.Matrix([1,0,0,0,0,0,0,0,0,1,0,0,0,0,1])
# coordinates ordered (12),(13),...,(56); use dictionary for explicit transform check
coords={ij:s.Integer(1 if ij in [(0,1),(2,3),(4,5)] else 0) for ij in itertools.combinations(range(6),2)}
g=s.diag(2,1,1,1,1,1);J2=g*J*g.T
assert J2.det()!=0
assert s.Matrix.hstack(s.Matrix([J[i,j] for i,j in coords]),s.Matrix([J2[i,j] for i,j in coords])).rank()==2
out={'symplectic_det':int(J.det()),'all_Grassmann_charts':results,'transformed_nonproportional':True}
Path('workspace/agent3_P5_counterexample_checks.json').write_text(json.dumps(out))
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_P5_counterexample_checks.py'):
 Path('workspace/agent3_P5_counterexample_checks.py').write_text(Path(__file__).read_text())
print('All 15 charts checked exactly; transformed sections nonproportional.')
