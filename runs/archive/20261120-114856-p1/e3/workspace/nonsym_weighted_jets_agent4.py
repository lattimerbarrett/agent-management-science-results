from sympy.polys.fields import field
from sympy import QQ,Rational as R,factor
import pickle
K,m,p,q1,q2=field('m,p,q1,q2',QQ);N=3;zero=K.zero;one=K.one
class J:
 def __init__(self,a):self.a=a if isinstance(a,list) else [K(a)]+[zero]*N
 def __add__(s,t):t=j(t);return J([a+b for a,b in zip(s.a,t.a)])
 __radd__=__add__
 def __neg__(s):return J([-a for a in s.a])
 def __sub__(s,t):return s+-j(t)
 def __rsub__(s,t):return j(t)+-s
 def __mul__(s,t):
  t=j(t);return J([sum((s.a[r]*t.a[k-r] for r in range(k+1)),zero) for k in range(N+1)])
 __rmul__=__mul__
 def __truediv__(s,t):
  t=j(t);o=[]
  for k in range(N+1):o.append((s.a[k]-sum((t.a[r]*o[k-r] for r in range(1,k+1)),zero))/t.a[0])
  return J(o)
 def __pow__(s,n):
  o=J(1)
  for k in range(n):o=o*s
  return o

def j(t):return t if isinstance(t,J) else J(t)
d=K(R(16267,5340));u=K(2);v=1+d;H=K(R(247,890));xis=[K(R(1,20)),K(3)]
# P=q q'-H: x4-Sx3+Tx2-Lx-H
S=u+v;T=d+u*v;L=u*d

def mp(state,bu,bb,bv,bd):
 mm,hh,zz,w1,w2=state;ws=[w1,w2]
 M=[J(1),mm,bu*mm-bb+hh]
 M.append(bu*M[2]-bb*mm+zz)
 for k in range(4,8):M.append(S*M[-1]-T*M[-2]+L*M[-3]+H*M[-4]-2*H*sum((xis[i]**(k-4)*ws[i] for i in range(2)),J(0)))
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[k+r] for r in range(5)),J(0)) for k in range(4)];norm=nums[0];ms=[nums[k]/norm for k in range(1,4)]
 return [ms[0],ms[1]-bv*ms[0]+bd,ms[2]-bv*ms[1]+bd*ms[0]]+[ws[i]*(xis[i]**2-a*xis[i]-b)**2/norm for i in range(2)]
e=J([zero,one,zero,zero]);a=mp([J(m),(1+(d-1)*p)/d*e,p*e,q1*e**2,q2*e**2],u,0,v,d);b=mp(a,v,d,u,0)
coef=[[x.as_expr() for x in row.a] for row in b]
pickle.dump(coef,open('workspace/nonsym_weighted_jets_agent4.pkl','wb'))
A=b[0].a[1];B=b[1].a[2];C=b[2].a[2];g=-d*B+(d-1)*C
F=[A,C+p*g,b[3].a[3]+2*q1*g,b[4].a[3]+2*q2*g]
pickle.dump(([x.as_expr() for x in F],g.as_expr()),open('workspace/nonsym_ode_agent4.pkl','wb'))
print('done',flush=True)
from pathlib import Path
Path('workspace/nonsym_weighted_jets_agent4.py').write_text(Path('scratchpad.py').read_text())
