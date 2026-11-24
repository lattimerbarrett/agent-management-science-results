"""Regenerate exact quadratic h-flow from orthogonal-polynomial moment equations (about 30 s)."""
import sympy as S,pickle
T=S.symbols('t');nodes=[-3,-S.sqrt(5),-1,1,S.sqrt(5),3]
a=[S.Rational(7,32),S.Rational(1,16),S.Rational(7,32),S.Rational(7,32),S.Rational(1,16),S.Rational(7,32)]
w=S.Matrix([wi*(1-T/x) for wi,x in zip(a,nodes)])
p=S.Matrix([x**4-10*x*x+11 for x in nodes]);q=p+12*S.ones(6,1);C=S.Integer(28)
V=S.Matrix([[x**j for j in range(4)] for x in nodes]);mul=lambda a,b:a.multiply_elementwise(b);simp=lambda a:a.applyfunc(S.cancel)
inv=simp((V.T*S.diag(*w)*V).inv());z=mul(w,mul(p,p))/C;ip=simp((V.T*S.diag(*z)*V).inv())
def flow(h):
 hv=V*h;u=mul(mul(w,p),hv)
 aa=simp(-V*inv*V.T*mul(u,p));bb=simp(-V*inv*V.T*mul(u,aa));F=(u.T*mul(p,p))[0];E=(u.T*mul(p,aa))[0]
 z1=simp((mul(u,mul(p,p))+2*mul(w,mul(p,aa))-z*F)/C)
 z2=simp((mul(w,mul(aa,aa)+2*mul(p,bb))+2*mul(u,mul(p,aa))-z1*F-z*E)/C)
 ab=simp(-V*ip*V.T*mul(z1,q));bb2=simp(-V*ip*V.T*(mul(z2,q)+mul(z1,ab)))
 Fb=(z1.T*mul(q,q))[0];Eb=(z2.T*mul(q,q)+z1.T*mul(q,ab))[0]
 o1=simp((mul(z1,mul(q,q))+2*mul(z,mul(q,ab))-w*Fb)/C)
 o2=simp((mul(z2,mul(q,q))+2*mul(z1,mul(q,ab))+mul(z,mul(ab,ab)+2*mul(q,bb2))-o1*Fb-w*Eb)/C)
 drift=simp(o1-u)
 return simp(ip/C*V.T*mul(p,o2-mul(drift,mul(p,hv))))
coeffs={}
for i in range(4): coeffs[(i,i)]=flow(S.eye(4)[:,i])
for i in range(4):
 for j in range(i+1,4): coeffs[(i,j)]=simp(flow(S.eye(4)[:,i]+S.eye(4)[:,j])-coeffs[(i,i)]-coeffs[(j,j)])
old=pickle.load(open('workspace/agent3_flip_hflow_exact.pkl','rb'))
assert all(simp(v-old['coeffs'][ij])==S.zeros(4,1) for ij,v in coeffs.items())
print('Full exact h-flow regenerated from moment equations and matched archived coefficients.')
