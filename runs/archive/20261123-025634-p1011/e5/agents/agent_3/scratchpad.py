import sympy as s
from pathlib import Path
m,k=s.symbols('m k',positive=True)
# Principal curvatures k,-k,0,... ; H=0.
scal=-2*k**2
W3434=0-(0+0)/(m-2)+scal/((m-1)*(m-2))
assert s.factor(W3434)==-2*k**2/((m-2)*(m-1))
for mv in range(4,40):
 principal=[s.Integer(1),s.Integer(-1)]+[s.Integer(0)]*(mv-2)
 H=sum(principal);ric=[x*(H-x)for x in principal];R=sum(ric)
 assert R==-2
 def W(i,j):return principal[i]*principal[j]-(ric[i]+ric[j])/s.Integer(mv-2)+R/s.Integer((mv-1)*(mv-2))
 assert W(2,3)==-s.Rational(2,(mv-1)*(mv-2))
 # Weyl traces vanish as a check of curvature convention.
 for i in range(mv):assert sum(W(i,j)for j in range(mv)if i!=j)==0
print('Verified intrinsic boundary Weyl obstruction in every m=4..39, with exact zero traces.')
import os,shutil
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_boundary_weyl_check.py'):
 shutil.copyfile(__file__,'workspace/agent3_boundary_weyl_check.py')
