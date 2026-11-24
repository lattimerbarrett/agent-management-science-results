import sys;sys.path.insert(0,'workspace')
from agent4_translation_exact import translation_model
import sympy as S,numpy as np,scipy.linalg as la,json,math
from pathlib import Path
t,p=S.symbols('t p')
def atan_bounds(inv,N=24):
 z=S.Rational(1,inv);v=sum((-1)**k*z**(2*k+1)/S.Integer(2*k+1)for k in range(N));r=(-1)**N*z**(2*N+1)/S.Integer(2*N+1)
 return min(v,v+r),max(v,v+r)
l5,u5=atan_bounds(5);l239,u239=atan_bounds(239);pilo=16*l5-4*u239;pihi=16*u5-4*l239

def mul(a,b):
 vals=[x*y for x in a for y in b];return min(vals),max(vals)
def interval(expr,tl,tu):
 expr=S.Poly(S.cancel(S.expand(expr*S.pi)).subs(S.pi,p),t)
 ans=(S.S.Zero,S.S.Zero)
 for c in expr.all_coeffs():
  pc=S.Poly(c,p);cc=(S.S.Zero,S.S.Zero)
  for v in pc.all_coeffs():
   cc=mul(cc,(pilo,pihi));cc=(cc[0]+v,cc[1]+v)
  ans=mul(ans,(tl,tu));ans=(ans[0]+cc[0],ans[1]+cc[1])
 return ans
results=[]
for n in range(21,33):
 d=2;m=n-1
 G1,G2,G3=translation_model(n,d)
 powers=S.Matrix(d+1,d+1,lambda i,j:2+2*i+2*j)
 D=G2.multiply_elementwise(powers)
 ev,vc=la.eigh(np.array(D.evalf(),float),np.array(G2.evalf(),float));v=vc[:,0]/vc[0,0]
 vq=S.Matrix([S.Rational(float(z)).limit_denominator(100000)for z in v])
 aa=S.Matrix([vq[j]*t**j for j in range(d+1)])
 cp=S.expand((aa.T*D*aa)[0])
 coeff=[float(c)for c in S.Poly(cp,t).all_coeffs()]
 roots=np.roots(coeff);root=min(z.real for z in roots if abs(z.imag)<1e-5 and z.real>0)
 tl=S.Rational(math.floor(root*10**7),10**7);tu=tl+S.Rational(1,10**7)
 assert interval(cp,tl,tl)[0]>0
 assert interval(cp,tu,tu)[1]<0
 assert interval(S.diff(cp,t),tl,tu)[1]<0
 # angular translation Hess polynomials, common positive P2 norm omitted.
 g=S.Matrix([aa[j]*(1+S.Rational(2*j,m+2))for j in range(d+1)])
 b=S.Matrix([2*(j+1)*aa[j+1]for j in range(d)])
 c=S.Matrix([2*(j+1)*(1+S.Rational(2*j,m+4))*aa[j+1] if j<d else 0 for j in range(d+1)])
 C=(aa.T*G2*c)[0]
 Hsupport=S.expand((m+2)*(g.T*G1*g)[0]+S.Rational(2*(m+1),(m+2)*(m+4))*(b.T*G3*b)[0]+3*C)
 Htrans=S.expand(S.Rational(1,m+4)*(b.T*G3*b)[0]+C)
 hs=interval(Hsupport,tl,tu);ht=interval(Htrans,tl,tu)
 assert hs[1]<0 and ht[1]<0
 print('CERTIFIED',n,list(vq),'root interval',tl,tu,'Hess upper',float(hs[1]),float(ht[1]))
 results.append({'n':n,'vector':[str(z)for z in vq],'t_lower':str(tl),'t_upper':str(tu),'scale_derivative':str(cp),'Hsupport':str(Hsupport),'Htrans':str(Htrans)})
Path('workspace/agent4_translation_certificates.json').write_text(json.dumps(results,indent=2))
