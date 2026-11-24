import sympy as s
from pathlib import Path
import json
H,P=s.symbols('H P')
D=6
a=s.Integer(2)
z=s.symbols('z2:'+str(D+2)) # z_k=ch_k(E) coefficient
hs=[s.Integer(1),H]
for i in range(2,D+1):hs.append(s.expand(H*hs[-1]-P*hs[-2]))
den=[hs[i]/s.factorial(i+1) for i in range(D+1)]
v=[]
for i in range(D+1):
 num=a if i==0 else z[i-1]*hs[i]
 v.append(s.expand(num-sum(den[j]*v[i-j] for j in range(1,i+1))))
cv=[s.Integer(1)]
for k in range(1,D+1):cv.append(s.expand(sum((-1)**(j-1)*s.factorial(j)*v[j]*cv[k-j] for j in range(1,k+1))/k))
print('c1V',cv[1]); print('c2V',s.factor(cv[2])); print('c3V',s.Poly(cv[3],H,P)); print('c4V',s.Poly(cv[4],H,P))
eq=[]
for k in range(3,D+1):
 eq.extend(s.Poly(cv[k],H,P).coeffs())
 gb=s.groebner(eq,*reversed(z[:k]))
 print('rank2 V degree',k,'GB',gb,flush=True)
 print('solutions',s.solve(list(gb),z[:k],dict=True),flush=True)
Path('workspace/agent2_rank2V_universal.py').write_text(Path(__file__).read_text())
