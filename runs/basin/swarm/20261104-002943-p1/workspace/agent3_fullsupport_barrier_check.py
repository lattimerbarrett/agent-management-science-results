import sympy as S
for N in [4,6,8]:
 u=S.symbols('u:'+str(N));e=S.symbols('e');ll=S.symbols('L:'+str(N-1));L=list(ll)+[1-sum(ll)]
 phi=S.log(1+2*e-sum(a*b for a,b in zip(L,u)))+sum(a*S.log(1+b) for a,b in zip(L,u))
 origin={e:0,**dict.fromkeys(u,0)}
 assert S.simplify(phi.subs(origin))==0
 assert S.simplify(S.diff(phi,e).subs(origin))==2
 assert all(S.simplify(S.diff(phi,v).subs(origin))==0 for v in u)
 print('N=',N,'all interpolation-error linear terms cancel; positive fuel derivative is exactly 2.')
