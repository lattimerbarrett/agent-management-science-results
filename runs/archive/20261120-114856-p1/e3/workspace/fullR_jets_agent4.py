from sympy.polys.fields import field
from sympy import QQ,Rational as R
import pickle,time
K,m,A,B,q,ell,k,T=field('m,A,B,q,ell,k,T',QQ);N=3;zero=K.zero;one=K.one
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
H=K(R(1,1000));U=K(R(3,4));Ts=[T,K(R(5,2))-T];Pconst=U*U-H

def mp(state,uu,vv):
 mm,hh,zz,s1,d1,s2,d2=state;ss=[s1,s2];ds=[d1,d2]
 M=[J(1),mm,uu*mm+U+hh];M.append(uu*M[2]+U*mm+zz)
 M +=[K(R(5,2))*M[2]-Pconst-2*H*(s1+s2),K(R(5,2))*M[3]-Pconst*mm-2*H*(d1+d2)]
 M +=[K(R(5,2))*M[4]-Pconst*M[2]-2*H*(Ts[0]*s1+Ts[1]*s2),K(R(5,2))*M[5]-Pconst*M[3]-2*H*(Ts[0]*d1+Ts[1]*d2)]
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[jj+r] for r in range(5)),J(0)) for jj in range(4)];norm=nums[0];ms=[nums[jj]/norm for jj in range(1,4)]
 out=[ms[0],ms[1]-vv*ms[0]-U,ms[2]-vv*ms[1]-U*ms[0]]
 for ti,si,di in zip(Ts,ss,ds):
  C=ti-b;F=C*C+a*a*ti
  out.extend([(si*F-2*a*C*di)/norm,(di*F-2*a*C*ti*si)/norm])
 return out
e=J([zero,one,zero,zero]);t0=time.time();aa=mp([J(m),A*e,B*e,q*e**2,ell*e**2,(1-q)*e**2,k*e**2],-1,1);print('first',time.time()-t0,flush=True);b=mp(aa,1,-1);print('second',time.time()-t0,flush=True)
gamma=(b[3].a[3]+b[5].a[3])/2
F=[b[0].a[1],b[1].a[2]-A*gamma,b[2].a[2]-B*gamma,b[3].a[3]-2*q*gamma,b[4].a[3]-2*ell*gamma,b[6].a[3]-2*k*gamma]
pickle.dump(([x.as_expr() for x in F],gamma.as_expr()),open('workspace/fullR_ode_agent4.pkl','wb'))
print('saved',time.time()-t0,flush=True)
from pathlib import Path
Path('workspace/fullR_jets_agent4.py').write_text(Path('scratchpad.py').read_text())
