from sympy.polys.fields import field
from sympy import QQ,factor
import pickle
K,m,p,q,ell=field('m,p,q,ell',QQ);N=3;zero=K.zero;one=K.one
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
def mp(state,U,V):
 mm,hh,zz,ss,dd=state
 M=[J(1),mm,U+hh,U*mm+zz]
 M+=[5*M[2]-2-4*ss,5*M[3]-2*mm-4*dd]
 M+=[5*M[4]-2*M[2]-8*ss,5*M[5]-2*M[3]-8*dd]
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[k+r] for r in range(5)),J(0)) for k in range(4)]
 norm=nums[0];ms=[nums[k]/norm for k in range(1,4)];C=2-b
 return [ms[0],ms[1]-V,ms[2]-V*ms[0],(ss*(C*C+2*a*a)-2*a*C*dd)/norm,(dd*(C*C+2*a*a)-4*a*C*ss)/norm]
e=J([zero,one,zero,zero]);a=mp([J(m),-e,p*e,q*e**2,ell*e**2],1,4);b=mp(a,4,1)
coef=[[factor(x.as_expr()) for x in row.a] for row in b]
for i,row in enumerate(coef):print(i,list(enumerate(row)),flush=True)
pickle.dump(coef,open('workspace/generic_weighted_jets_agent4.pkl','wb'))
from pathlib import Path
Path('workspace/generic_weighted_jets_agent4.py').write_text(Path('scratchpad.py').read_text())
