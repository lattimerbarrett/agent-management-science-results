from pathlib import Path
exec(Path('experiments/e1/agent2_sr1_counterexample_checks.py').read_text())
import sympy as s
for N in range(2,25):
 P=s.zeros(N);P[0,0]=1
 assert P.norm(2)==1
 assert s.trace(P)/N==s.Rational(1,N)
print('The rank-one projections have norm 1 and normalized trace 1/N.')
print('In the norm product quotient their class is nonzero, but has m orthogonal equivalent copies for every fixed m.')
