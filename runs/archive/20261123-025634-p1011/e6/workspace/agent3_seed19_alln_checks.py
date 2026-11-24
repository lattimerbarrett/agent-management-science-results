"""Exact certificate: explicit stable quadratic-reduction graph seeds for all n>=19.
NOT a proof of Yamabe noncompactness: moving-domain energy expansion remains separate.
Run symbolic_q2_generate.py and symbolic_trans_generate.py first to regenerate input.
"""
import sympy as s,pickle,sys
sys.path.insert(0,'workspace')
import agent3_odd_gram_checks as c
from fractions import Fraction as F
n,t,a0,x=s.symbols('n t a0 x');m=n-1
with open('workspace/agent3_symbolic_q2.pkl','rb') as f:r=pickle.load(f)
with open('workspace/agent3_symbolic_trans_M.pkl','rb') as f:tr=pickle.load(f)
M2=s.zeros(4)
for (i,j),(u,v) in r.items():M2[i,j]=M2[j,i]=u+t*v
Ms={}
for q,dd in tr.items():
 M=s.zeros(3)
 for (i,j),v in dd.items():M[i,j]=M[j,i]=v
 Ms[q]=M
K=s.Matrix(4,4,lambda i,j:(i+j+1)*M2[i,j]);T=s.Matrix(4,4,lambda i,j:(i+j)*(i+j+1)*M2[i,j])
a=s.Matrix([a0,-s.Rational(230,499),s.Rational(46,821),-s.Rational(1,722)])
P=(a.T*K*a)[0];Hs=-(a.T*T*a)[0]
checks={'-Plo':-P.subs(a0,s.Rational(27,25)),'Phi':P.subs(a0,s.Rational(117,100)),'Hslo':Hs.subs(a0,s.Rational(27,25)),'Hs_slope':s.diff(Hs,a0)}
g=s.Matrix([a[i]*(1+s.Rational(2*i,1)/(m+2)) for i in range(1,4)])
fp=s.Matrix([i*a[i] for i in range(1,4)])
for z in [0,1]:
 r1=(m+2)*z;r3=(3/(m+4)-1/(m+2)) if z else 1/(m+4)
 b=s.zeros(4,1)
 for i in range(3):b[i]=(2+4*z)*fp[i]
 for i in range(2,4):b[i-1]+=(4+8*z)/(m+4)*i*(i-1)*a[i]
 H=-(r1*(g.T*Ms[1]*g)[0]+4*r3*(fp.T*Ms[3]*fp)[0]+(a.T*M2*b)[0])
 assert s.diff(H,a0,2)==0
 checks[f'Htrans{z}lo']=H.subs(a0,s.Rational(27,25));checks[f'Htrans{z}slope']=s.diff(H,a0)
U=8*n/(3*(n-1)**2)
for name,e in checks.items():
 assert s.diff(e,t,2)==0
 for tv in [0,U]:
  nu,de=s.fraction(s.factor(e.subs(t,tv)))
  pp=s.Poly(nu.subs(n,x+29),x);qq=s.Poly(de.subs(n,x+29),x)
  assert all(v>=0 for v in pp.all_coeffs()) and pp.nth(0)>0,name
  assert all(v>=0 for v in qq.all_coeffs()) and qq.nth(0)>0,name
print('All 16 infinite-family polynomial coefficient certificates passed: n>=29.')
for N in range(19,29):
 tg=s.simplify(4*s.gamma(s.Rational(N-1,2))**2/(s.pi*s.gamma(s.Rational(N,2))**2))
 if tg.is_Rational:ti=c.point(F(tg))
 else:
  coeff=s.simplify(tg*s.pi**2);assert coeff.is_Rational
  ti=(F(coeff)/c.PI[1]**2,F(coeff)/c.PI[0]**2)
 for name,e in checks.items():
  e=s.factor(e.subs(n,N));e0=e.subs(t,0);e1=s.diff(e,t)
  assert e0.is_Rational and e1.is_Rational
  interval=c.plus(c.point(F(e0)),c.times(c.point(F(e1)),ti))
  assert interval[0]>0,(N,name,interval)
 print('All eight finite-dimensional seed inequalities passed, n=',N)
print('CERTIFIED: centered stable quadratic-reduction seed exists in every n>=19.')
