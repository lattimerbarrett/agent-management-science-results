import sympy as S
from pathlib import Path
s,t,a,b=S.symbols('s t a b',real=True)
q=S.Matrix([S.cos(t)*S.sin(s),S.sin(t),S.cos(t)*S.cos(s)])
e1=S.Matrix([S.cos(s),0,-S.sin(s)])
e2=S.Matrix([-S.sin(t)*S.sin(s),S.cos(t),-S.sin(t)*S.cos(s)])
p=a*e1+b*e2
simp=lambda e:S.trigsimp(S.expand_trig(e))
assert simp(q.dot(q)-1)==0
assert simp(e1.dot(e1)-1)==0
assert simp(e2.dot(e2)-1)==0
assert simp(q.dot(e1))==simp(q.dot(e2))==simp(e1.dot(e2))==0
assert simp(p.dot(p)-a*a-b*b)==0
f=-2*(a*S.sin(s)+b*S.sin(t)*S.cos(s))
assert simp(2*p[2]-f)==0
Y=[S.sin(s)*S.cos(s)/2,t/2,(1-S.cos(s)**2/2)*a,(1+S.sin(s)**2/2-t*S.cot(t)/2)*b]
assert simp(sum(v*S.diff(f,z) for v,z in zip(Y,[s,t,a,b]))-f)==0
# Squared radius in the last two coordinates strictly increases away from0:
rprime=S.expand(2*a*Y[2]+2*b*Y[3])
assert simp(rprime-(a*a*(1+S.sin(s)**2)+b*b*(2+S.sin(s)**2-t*S.cot(t))))==0
assert S.limit(t*S.cot(t),t,0)==1
# Full normal-radius derivative exceeds its squared radius on |t|<pi/2,
# since t*cot(t)<=1 there (equivalent to sin(t)>=t*cos(t)).
R2=t*t+a*a+b*b
YR2=2*t*Y[1]+rprime
assert simp(YR2-R2-(a*a*S.sin(s)**2+b*b*(1+S.sin(s)**2-t*S.cot(t))))==0
# Exact defining-function identity for the ellipsoidal smooth ball.
A,r=S.symbols('A r',positive=True)
u=s-S.pi/2
rho=u*u/A**2+R2/r**2
Yrho=sum(v*S.diff(rho,z) for v,z in zip(Y,[s,t,a,b]))
assert simp(Yrho-(u*S.sin(s)*S.cos(s)/A**2+YR2/r**2))==0
# Outward inequalities at s faces and t faces, choose delta=pi/12.
d=S.pi/12
assert S.simplify(Y[0].subs(s,-d))<0
assert S.simplify(Y[0].subs(s,S.pi+d))>0
assert S.simplify(Y[1].subs(t,-d))<0
assert S.simplify(Y[1].subs(t,d))>0
print('All exact symbolic checks passed: orthonormal frame, product-sphere coordinates, f formula, Yf=f, strict outward face inequalities.')
# Save reproducible script.
Path('workspace/adapted_ball_agent2.py').write_text(Path('scratchpad.py').read_text().split('# Save reproducible script.')[0])
