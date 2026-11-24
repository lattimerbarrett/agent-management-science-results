import sympy as S
from sympy.functions.combinatorial.numbers import stirling
from pathlib import Path
q,h,delta,E,WA,WB,w=S.symbols('q h delta E WA WB w')

def expansion(d):
 u=q+d
 U=(u*(u-1)+q*(q+1))/2
 V=d*q*(q+1)/2+(u*(u-1)*(2*u-1)+q*(q+1)*(2*q+1))/12
 FF={0:S.Integer(1) if d==0 else h,1:2*h if d==0 else S.Integer(1)}
 for k in range(1,15):FF[k+1]=S.expand(2*FF[k-1]-k*FF[k])
 for k in range(1,15):FF[-k]=FF[k]/2**k
 def T(r,s,P=1):
  P=S.Poly(S.expand(S.sympify(P).subs(q,q+s)),q);ans=0
  for (j,),c in P.terms():
   for ell in range(j+1):ans+=c*stirling(j,ell,kind=2)*FF[d+s-r+ell]
  return S.expand(ans)
 PA=2*delta*w-S.Rational(7,2)*w*w
 QA=(-6*delta-2*WA)*w*w+S.Rational(26,3)*w**3
 PB=2*E*w-S.Rational(1,2)*w*w
 QB=(-6*E-2*WB)*w*w+S.Rational(1,3)*w**3
 def tsum(A,B,P=1):
  ans=0
  for (r,),a in S.Poly(A,w).terms():
   for (s,),b in S.Poly(B,w).terms():ans+=a*b*T(r,s,P)
  return S.expand(ans)
 H1=tsum(PA,1)+tsum(1,PB)+T(0,0,U)
 H2=tsum(QA+PA*PA/2,1)+tsum(PA,PB)+tsum(1,QB+PB*PB/2+d*PB)+tsum(PA,1,U)+tsum(1,PB,U)+T(0,0,V+U*U/2)
 log2=S.expand(H2-H1*H1/2)
 graphlog2=S.expand(log2-log2.subs({delta:0,E:0,WA:0,WB:0}))
 return S.expand(H1),S.factor(graphlog2)
for d in [0,1]:
 x,y=expansion(d)
 print('d',d,'H1=',x,'\ngraphlog2=',S.collect(S.expand(y),[delta,E,WA,WB]))
 if d==0:
  diff=S.expand(y.subs({delta:-S.Rational(1,2),E:2,WA:0,WB:0})-y.subs({delta:S.Rational(7,2),E:0,WA:28,WB:0}))
  import mpmath as mp
  hv=mp.besseli(1,2*mp.sqrt(2))/(mp.sqrt(2)*mp.besseli(0,2*mp.sqrt(2)))
  print('star9-vs2Bedge predicted n2 gain',S.factor(4*diff),float((4*diff).subs(h,float(hv))))
