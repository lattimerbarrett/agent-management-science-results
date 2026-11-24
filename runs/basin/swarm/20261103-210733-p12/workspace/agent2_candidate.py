import sys,io,contextlib,json
sys.path.insert(0,'workspace')
with contextlib.redirect_stdout(io.StringIO()):import fz25_upper as F
from sympy import Matrix,Rational
from sympy.polys.matrices import DomainMatrix
F.k0=46
r=F.rel(10,(1,))
v={tuple(sorted(q+(2,),reverse=True)):c for q,c in r.items()}
d=json.load(open('workspace/agent2_Pgood.json'))
assert [str(v.get(p,0)) for p in F.partitions(12)]==d['vector']
fz=json.load(open('workspace/fz25_upper_data.json'))
M=Matrix([[Rational(c) for c in row] for row in fz['matrix']]+[[Rational(c) for c in d['vector']]])
assert DomainMatrix.from_Matrix(M).rank()==34
print('Pgood verified as κ2 times genus24 FZ relation r10 sigma1, and nonzero modulo genus25 FZ.')
