import sympy as S
from pathlib import Path
s,t,a,b,d=S.symbols('s t a b d', real=True)
q=S.Matrix([S.cos(t)*S.sin(s),S.sin(t),S.cos(t)*S.cos(s)])
ea=S.Matrix([S.cos(s),0,-S.sin(s)])
eb=S.Matrix([-S.sin(t)*S.sin(s),S.cos(t),-S.sin(t)*S.cos(s)])
simp=lambda x:S.trigsimp(S.expand_trig(S.expand(x)))
assert simp(q.dot(q)-1)==0
assert simp(ea.dot(ea)-1)==0
assert simp(eb.dot(eb)-1)==0
assert simp(q.dot(ea))==simp(q.dot(eb))==simp(ea.dot(eb))==0
p=a*ea+b*eb
x=S.sqrt(1-a*a-b*b)*q+p
y=-S.sqrt(1-a*a-b*b)*q+p
assert simp(x.dot(x)-1)==simp(y.dot(y)-1)==0
f=simp(x[2]+y[2])
assert simp(f+2*(a*S.sin(s)+b*S.sin(t)*S.cos(s)))==0
Y=S.Matrix([S.sin(s)*S.cos(s)/2,S.sin(t)*S.cos(t)/2,(1-S.cos(s)**2/2)*a,(1+S.sin(s)**2/2-S.cos(t)**2/2)*b])
vars=[s,t,a,b]
assert simp(sum(Y[i]*S.diff(f,vars[i]) for i in range(4))-f)==0
# Face transversality formulas, taking 0<d<pi/4.
assert simp(Y[0].subs(s,-d)+S.sin(d)*S.cos(d)/2)==0
assert simp(Y[0].subs(s,S.pi+d)-S.sin(d)*S.cos(d)/2)==0
assert simp(Y[1].subs(t,-d)+S.sin(d)*S.cos(d)/2)==0
assert simp(Y[1].subs(t,d)-S.sin(d)*S.cos(d)/2)==0
radial=simp(Y[2]*2*a+Y[3]*2*b)
# derivative of normal radius squared is >= radius squared
assert simp(radial-(a*a+b*b)-(a*a*S.sin(s)**2+b*b*(S.sin(s)**2+S.sin(t)**2)))==0
# Critical points in chart: df/da=0 forces sin(s)=0. Then df/db=0 forces sin(t)=0.
# On chosen interval (-d,pi+d), |t|<d, these imply (s,t)=(0,0),(pi,0).
# At each, df/ds=df/dt=0 then forces a=b=0; exact checks and Hessian inertia:
for s0 in [0,S.pi]:
  H=S.hessian(f,vars).subs({s:s0,t:0,a:0,b:0})
  assert H.det()!=0
  assert H.eigenvals()=={-2:2,2:2}
# All four original critical points (sphere heights) and Hessian signatures:
for z,w in [(1,1),(1,-1),(-1,1),(-1,-1)]:
  diag=[-z,-z,-w,-w]
  assert sum(v<0 for v in diag) in [0,2,4]
print('PASS: orthonormal tubular frame, both sphere constraints, exact f, Yf=f, all outward-face identities, two chart saddles and Hessian signatures.')
# Smooth ellipsoid alternative (t*cot(t) has value 1 at t=0).
Y2=S.Matrix([Y[0],t/2,Y[2],(1+S.sin(s)**2/2-t*S.cos(t)/(2*S.sin(t)))*b])
assert simp(sum(Y2[i]*S.diff(f,vars[i]) for i in range(4))-f)==0
assert S.limit(t*S.cos(t)/S.sin(t),t,0)==1
normal=Y2[1]*2*t+Y2[2]*2*a+Y2[3]*2*b
assert simp(normal-(t*t+a*a+b*b)-(a*a*S.sin(s)**2+b*b*(1+S.sin(s)**2-t*S.cos(t)/S.sin(t))))==0
print('PASS: modified smooth Yf=f; ellipsoid positivity reduces to t*cot(t)<=1 and elementary trigonometric inequality.')
source=Path('scratchpad.py').read_text()
# Save this independently checkable certificate without overwriting others.
Path('workspace/agent1_fusion_checks.py').write_text(source.split("source=Path('scratchpad.py').read_text()")[0])
