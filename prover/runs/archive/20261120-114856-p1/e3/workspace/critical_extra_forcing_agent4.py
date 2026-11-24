from pathlib import Path
import sympy as s,pickle,time
from sympy.polys.fields import field
K,z,t=field('z,t',s.QQ);H=-t*t*(t-1)*(t-4)
class D:
 def __init__(self,a,b=0):self.a=K(a);self.b=K(b)
 def __add__(self,o):o=co(o);return D(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return D(-self.a,-self.b)
 def __sub__(self,o):return self+-co(o)
 def __rsub__(self,o):return co(o)+-self
 def __mul__(self,o):o=co(o);return D(self.a*o.a,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __truediv__(self,o):o=co(o);return D(self.a/o.a,(self.b*o.a-self.a*o.b)/(o.a*o.a))
 def __rtruediv__(self,o):return co(o)/self
 def __pow__(self,n):
  if n==0:return D(1)
  return D(self.a**n,n*self.a**(n-1)*self.b)
def co(x):return x if isinstance(x,D)else D(x)
M=[K(1),1-z,1-z,1-z]
for j in range(4,12):M.append(5*M[j-1]-4*M[j-2]+H*M[j-4])
mu=[D(M[j],t**j-M[j])for j in range(12)]
def T(mm):
 m,m2,m3=mm[1:4];a=(m3-m*m2)/(m2-m*m);b=m2-a*m;pp=[-b,-a,D(1)];ss=[sum((pp[j]*pp[k-j]for j in range(max(0,k-2),min(2,k)+1)),D(0))for k in range(5)];num=[sum((ss[k]*mm[j+k]for k in range(5)),D(0))for j in range(len(mm)-4)];return [x/num[0]for x in num]
start=time.time();mm=T(T(mu));DM=[mm[j].b-(t**j-M[j])for j in range(4)];df2=DM[1];df1=DM[2]-5*DM[1];df0=DM[3]-5*DM[2]+4*DM[1];dz=-(df2*z*z+df1*z+df0)/(z*(z-4));dc=df2+dz;dd=df1-4*dz+z*dc
assert DM[2]-DM[1] ==4*t*(t-1)
assert DM[3]-DM[2] ==4*t*t*(t-1)
assert dd+4*dc ==-4*t*t*(t-1)/(z-4)
assert -dc ==4*t*(t-1)*(t+z-4)/(z*(z-4))
assert dz ==dc-DM[1]
assert 3*(DM[3]-DM[2]) ==12*t*t*(t-1)
assert 3*(4-z)*(dd+4*dc) ==12*t*t*(t-1)
assert (t*(t-1)*t*(t-4)/H)**2 ==1
print('8 exact rational identities ASSERTED')
for name,val in [('dm',DM[1]),('dz',dz),('dc',dc),('dd',dd),('drho',-dc),('ddelta',dd+4*dc)]:print(name,s.factor(val.as_expr()))
print('time',time.time()-start);pickle.dump((z.as_expr(),t.as_expr(),{name:s.factor(val.as_expr())for name,val in [('dm',DM[1]),('dz',dz),('dc',dc),('dd',dd),('drho',-dc),('ddelta',dd+4*dc)]}),open('workspace/critical_extra_forcing_agent4.pkl','wb'))
