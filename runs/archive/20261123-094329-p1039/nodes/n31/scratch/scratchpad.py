from pathlib import Path
p=Path('experiments/e2/agent1_graph_disk_check.py')
exec(compile(p.read_text(),str(p),'exec'))
import sympy as s
eps=1/(32*s.pi); delta=eps**2/4
print('epsilon =',eps,'delta =',delta)
print('Graph contraction rho max:',s.simplify(delta-eps**2))
print('Excluded point rho:',s.simplify(2/s.pi**2+delta/4-eps**2))
print('Uniform Levi determinant lower bound:',s.simplify(1+delta-8*s.pi*eps))
print('The whole graph contraction lies in rho <= -epsilon^2/2:',s.simplify(delta-eps**2)<=-eps**2/2)
