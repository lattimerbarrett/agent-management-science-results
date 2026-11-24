import sympy as S,pickle
from pathlib import Path
z=S.symbols('z')
d=pickle.load(open('workspace/agent4_nonmax_normal_jet.pkl','rb'));nodes=d['x'];qv=d['q'];Qv=d['Q'];w=d['w0'];C=d['C'];Delta=S.prod(z-a for a in nodes)
p=S.interpolate(list(zip(nodes,qv)),z);q=S.interpolate(list(zip(nodes,Qv)),z)
f=S.interpolate([(a,S.factor(wi*S.diff(Delta,z).subs(z,a)/Qi)) for a,wi,Qi in zip(nodes,w,Qv)],z)
assert S.degree(f,z)==3 and S.LC(S.Poly(f,z))==1
print('f=',S.factor(f))
a,b,c=S.symbols('a b c');df=a+b*z+c*z*z
left=S.expand(sum((p.subs(z,t)+q.subs(z,t))*df.subs(z,t)**2/(S.diff(Delta,z).subs(z,t)*f.subs(z,t)) for t in nodes))/4
inv=S.invert(Delta,f,z);rem=S.rem((p+q)*df**2*inv,f,z)
right=-S.Poly(rem,z).coeff_monomial(z**2)/4
assert S.expand(left-right)==0
print('Exact weightedFisher/Staeckel residue identity PASS')
