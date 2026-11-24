"""Exact symbolic check of agent3 reduced K,F equations.
Inputs are exact symbolic jet coefficients independently computed from moment solves.
"""
import sympy as S,pickle
nf=pickle.load(open('workspace/agent3_flip_Kflow_exact.pkl','rb'));ff=pickle.load(open('workspace/agent3_flip_Kforce_exact.pkl','rb'))
t=nf['t'];k0,k1,k2,F=nf['vars'];m=ff['m'];Kt=k0+k1*t+k2*t*t
D=(t*t-1)*(t*t-5)*(t*t-9);P=t**4-10*t*t+11;Q=P+12;R=P*Q;P0=P+6;v=D*Kt/14
pred=S.Matrix([v*((2*t*(t*t+5)/7+20*t*P0/R)*Kt-k1-t*k2),v*(2*(t*t-5)*Kt/7-k2),-4*t*v*(S.Rational(1,7)+P0/R)*Kt,-v*P0*Kt])
assert all(S.cancel(a-b)==0 for a,b in zip(pred,nf['flow']))
pm=m**4-10*m*m+11
j=48*(m+t)*(m*m+t*t-10)*pm/R
b2=-12*(m+t)*pm*((m*m-5)*D-28)/(7*R)
b1=12*(m*m-5)*pm/7
force=S.Matrix([j-t*b1-t*t*b2,b1,b2,-48*pm])
assert all(S.cancel(a-b)==0 for a,b in zip(force,ff['force']))
# Derived no-flip conserved momentum: J=K(t)*sqrt(P(t)Q(t)).
dKt=pred[0]+t*pred[1]+t*t*pred[2]+(k1+2*t*k2)*v
assert S.cancel(dKt+Kt*S.diff(R,t)*v/(2*R))==0
# Recheck reduced field equals moving-base transformation of full exact h-jet.
hh=pickle.load(open('workspace/agent3_flip_hflow_exact.pkl','rb'));ph=pickle.load(open('workspace/agent4_flip_physical.pkl','rb'));hv=ph['hvars'];h=S.Matrix(hv);T=ph['T'];qq=sum((co*hv[i]*hv[j] for (i,j),co in hh['coeffs'].items()),S.zeros(4,1))
raw=T*qq+T.diff(t)*h*ph['v'];subs=dict(zip(nf['vars'],T*h));back=pred.subs(subs,simultaneous=True)
assert all(S.cancel(a-b)==0 for a,b in zip(raw,back))
print('Exact reduced no-flip field, flip-force coefficients, transformation, and conserved no-flip momentum verified.')
