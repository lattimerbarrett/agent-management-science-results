import sympy as s,pickle,time
from pathlib import Path
z,c=s.symbols('z c');S=s.Integer(5);Q=s.Integer(4);H=s.Rational(1863,4096)
def simp(x):return s.cancel(x)
class J:
 def __init__(self,a,b=0,d=0):self.t=[simp(a),simp(b),simp(d)]
 def __add__(self,o):
  if not isinstance(o,J):o=J(o)
  return J(*[self.t[k]+o.t[k]for k in range(3)])
 __radd__=__add__
 def __neg__(self):return J(*[-x for x in self.t])
 def __sub__(self,o):return self+-o if isinstance(o,J) else self+(-o)
 def __rsub__(self,o):return -self+o
 def __mul__(self,o):
  if not isinstance(o,J):o=J(o)
  return J(*[sum(self.t[j]*o.t[k-j]for j in range(k+1))for k in range(3)])
 __rmul__=__mul__
 def inv(self):
  a,b,d=self.t;return J(1/a,-b/a**2,b*b/a**3-d/a**2)
 def __truediv__(self,o):return self*(o.inv()if isinstance(o,J)else J(1/o))
 def __rtruediv__(self,o):return self.inv()*o

def f(z,c,d):
 m=S+c-z;M2=d-c*z+S*m-Q;M3=-d*z+S*M2-Q*m;A=(m*M2-M3)/(M2-m*m);B=-M2-A*m;HH=H+B*d-z*(A*d+B*c);ZZ=(B*d*z-(m+A)*H)/HH
 return ZZ,A,B
def ds(c):return c*(Q+S*c+c*c)/(S+2*c)
start=time.time();F=f(J(z),J(c),J(ds(c),1));print('first done',time.time()-start,flush=True)
G=f(*F);print('second done',time.time()-start,flush=True)
DD=G[2]-ds(G[1]);res=[G[0]-z,G[1]-c,DD]
for name,vv in zip(['zshift','cshift','delta'],res):
 print(name,[(i,s.factor(x))for i,x in enumerate(vv.t)],flush=True)
pickle.dump((z,c,res[0].t,res[1].t,DD.t),open('workspace/critical_defect_jets_agent2.pkl','wb'))
Path('workspace/critical_defect_jets_agent2.py').write_text(Path(__file__).read_text())
