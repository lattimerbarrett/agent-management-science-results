from itertools import combinations
import sympy as s
F0=[{0,1,2},{0,1,3},{2,3,4},{2,3,5},{0,4,5},{1,4,5}]
cores=[{0,1},{2,3},{4,5}]
vals=[]
for L in range(4):
 P=[set(range(6+i*L,6+(i+1)*L)) for i in range(3)]
 F=[A|P[next(i for i,X in enumerate(cores) if X<=A)] for A in F0]
 cnt=sum(all(set(C)&A for A in F) for C in combinations(range(6+3*L),3));vals.append((3+L,cnt)); print(L,cnt)
x=s.symbols('K');p=s.interpolate(vals,x);print(s.factor(p));print([p.subs(x,i) for i in range(4)])
assert s.expand(p)==x**3-3*x**2+6*x-4
import pathlib
pathlib.Path('workspace/agent4_padding_polynomial.py').write_text(pathlib.Path('scratchpad.py').read_text())
