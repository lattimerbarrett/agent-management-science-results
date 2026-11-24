from sympy.polys.fields import field
from sympy import QQ,Rational as R,factor
import pickle,time
K,m,p,q=field('m,p,q',QQ); N=6
zero=K.zero;one=K.one
class Jet:
 def __init__(self,x):self.a=x if isinstance(x,list) else [K(x)]+[zero]*N
 def __add__(self,y):
  y=y if isinstance(y,Jet) else Jet(y);return Jet([a+b for a,b in zip(self.a,y.a)])
 __radd__=__add__
 def __neg__(self):return Jet([-x for x in self.a])
 def __sub__(self,y):return self+-asjet(y)
 def __rsub__(self,y):return asjet(y)+-self
 def __mul__(self,y):
  y=asjet(y);return Jet([sum((self.a[j]*y.a[k-j] for j in range(k+1)),zero) for k in range(N+1)])
 __rmul__=__mul__
 def __truediv__(self,y):
  y=asjet(y);out=[]
  for k in range(N+1):out.append((self.a[k]-sum((y.a[j]*out[k-j] for j in range(1,k+1)),zero))/y.a[0])
  return Jet(out)
 def __pow__(self,n):
  out=Jet(1)
  for j in range(n):out=out*self
  return out

def asjet(y):return y if isinstance(y,Jet) else Jet(y)
u=K(1);v=K(4);xi=K(R(9,8));H=K(R(1863,4096))
e=Jet([zero,one]+[zero]*(N-1))
def mp(M,base_u,base_v):
 mm,hh,zz,ww=M
 moms=[Jet(1),mm,base_u*mm+hh,base_u*base_u*mm+base_u*hh+zz]
 for j in range(4,8):moms.append((u+v)*moms[-1]-u*v*moms[-2]+H*moms[-4]-2*H*xi**(j-4)*ww)
 a=(moms[3]-mm*moms[2])/(moms[2]-mm*mm);b=moms[2]-a*mm
 Q=[b*b,2*a*b,a*a-2*b,-2*a,Jet(1)]
 nums=[sum((Q[j]*moms[k+j] for j in range(5)),Jet(0)) for k in range(4)]
 den=nums[0];nms=[nums[k]/den for k in range(1,4)]
 return [nms[0],nms[1]-base_v*nms[0],nms[2]-base_v*nms[1],ww*(xi*xi-a*xi-b)**2/den]
print('start',flush=True);t0=time.time()
a=mp([Jet(m),e,p*e**2,q*e**4],u,v);print('first',time.time()-t0,flush=True)
b=mp(a,v,u);print('second',time.time()-t0,flush=True)
for i in range(4):
 print('OUTPUT',i,flush=True)
 for j in range(N+1):
  if b[i].a[j]:print(j,factor(b[i].a[j].as_expr()),flush=True)
pickle.dump([[x.as_expr() for x in row.a] for row in b],open('workspace/weighted_jets_agent4.pkl','wb'))
from pathlib import Path
Path('workspace/weighted_jets_agent4.py').write_text(Path('scratchpad.py').read_text())
