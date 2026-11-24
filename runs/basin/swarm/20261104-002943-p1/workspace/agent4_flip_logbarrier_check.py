import sympy as S
from pathlib import Path
z=S.symbols('z');r=S.sqrt(14);aa=S.sqrt(6-r);bb=S.sqrt(6+r);nodes=[-bb,-aa,aa,bb,S.Integer(2)];P=z*z-3;Q=z*z-9;C=S.Integer(5);D=(P*Q-C).expand();DT=S.expand(D*(z-2));bet=[S.simplify(1/S.diff(DT,z).subs(z,x)) for x in nodes];alph=bet[:4]+[-bet[4]]
assert bet[4]==-S.Rational(1,10) and S.simplify(sum(alph)-1/C)==0
a,b,c,d,h=S.symbols('a b c d h');pp=z*z+a*z+b;qq=z*z+c*z+d;R=S.expand(pp*qq)
assert S.simplify(sum(v*R.subs(z,x) for v,x in zip(bet,nodes))-1)==0
Z=[R.subs(z,x)/h for x in nodes[:4]]+[-R.subs(z,nodes[4])/h]
assert S.simplify(sum(v*m for v,m in zip(alph,Z))-1/h)==0
# Exact interpolation for arbitrary degree<=3 perturbation of monic product.
err=R-P*Q;LI=[]
for i,x in enumerate(nodes[:4]):LI.append(S.prod((nodes[4]-y)/(x-y) for j,y in enumerate(nodes[:4]) if j!=i))
assert S.simplify(err.subs(z,nodes[4])-sum(L*err.subs(z,x) for L,x in zip(LI,nodes[:4])))==0
print('Full2sfliplogbarrier algebra PASS; beta_mu=',bet[-1],'; sumalpha=',S.simplify(sum(alph)))
