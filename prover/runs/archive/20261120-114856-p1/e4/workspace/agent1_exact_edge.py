import sympy as S,itertools,pickle
from pathlib import Path
u=S.symbols('u');xs=[-8,-7,-4,-1,1,4,7,8];ts=[S.Rational(x,8) for x in xs]
p=[S.Rational(x**4-65*x*x+424,360) for x in xs];q=S.Matrix([pi+S.Rational(1,2) for pi in p]);r=S.Matrix([pi-S.Rational(1,2) for pi in p]);H=S.Rational(3,4)
f=S.Matrix([[t**j for j in range(4)] for t in ts]);B=S.ones(1,8).col_join(f.T*S.diag(*q));target=S.Matrix([1,0,0,0,0]);verts=[]
for inds in itertools.combinations(range(8),5):
 BB=B[:,inds]
 if not BB.det():continue
 ww=BB.inv()*target
 if min(ww)>0:
  w=S.zeros(8,1)
  for i,v in zip(inds,ww):w[i]=v
  verts.append((inds,w))
print('vertexsupports',[v[0] for v in verts],flush=True)
V0,W0=verts[0]
V1,W1=next((i,w) for i,w in verts if len(set(i)|set(V0))==6)
dW=W1-W0;W=W0+u*dW
G=f.T*S.diag(*W)*f;Wp=S.diag(*[qi**2/H for qi in q])*W;Gp=f.T*S.diag(*Wp)*f
DR=-(Gp.inv()*G).applyfunc(S.cancel)
dh=(S.ones(1,8)*S.diag(*W)*S.diag(*list(r-q))*f)
EM=(S.diag(*r)*f+S.diag(*q)*f*DR-S.ones(8,1)*dh).applyfunc(S.cancel)
i=next(i for i in range(8) if dW[i]!=0)
a=(2*W[i]/(H*dW[i])*EM[i,:]).applyfunc(S.cancel)
for j in range(8):assert (2*W[j]*EM[j,:]/H-dW[j]*a).applyfunc(S.cancel)==S.zeros(1,4)
vect=S.zeros(4,1)
for j in range(8):
 if dW[j]:vect+=q[j]*f[j,:].T*dW[j]**2/W[j]
Bc=(G.inv()*vect/4).applyfunc(S.cancel)
K=(-Bc*a).applyfunc(S.factor)
print('edge',V0,V1,'a=',a.applyfunc(S.factor),flush=True)
print('B=',Bc.applyfunc(S.factor),flush=True)
print('Kdenominators',sorted(set(str(S.factor(S.denom(v))) for v in K)),flush=True)
print('K',K,flush=True)
for end in [0,1]:
 lim=K.applyfunc(lambda x:S.cancel(x).subs(u,end))
 assert not any(x.has(S.zoo,S.nan,S.oo) for x in lim)
 print('endpoint',end,'trace',S.factor(S.trace(lim)))
