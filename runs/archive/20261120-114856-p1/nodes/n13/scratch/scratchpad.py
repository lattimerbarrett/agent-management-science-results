import sympy as S
# Expand the projective two-block map for m=s+1 base nodes plus one extra node.
z=S.symbols('z')
H,B,C,Q,E,a,h,w=S.symbols('H B C Q E a h w', nonzero=True)
# p_i(0)=h/(H*w); dlog p_i/dz = B**2/H-B*a.
dp=B**2/H-B*a
# unnormalized first-block base weights W_i=h_i^2/(H^2*w_i)
# H1=sum h_i^2/W_i=H^2; B1=sum h_i*l_i/W_i=H^2*Q
# derivatives H1'/H1 = -2 sum w_i dp_i= -2*(B**2/H-B*Q)
# second polynomial coefficient log-derivative includes moving W and extra weight Z=z*B^2/H^2
# q_i baseline H*w/h; q_i relative derivative:
# -dlog W_i -dlog H1 + (dZ/dz)*(B1**2/H1-B1*a)
dq=-2*dp+2*(B**2/H-B*Q)+(B**2/H**2)*(H**2*Q**2-H**2*Q*a)
# Wait unnormalized second q baseline w/h (not H*w/h): H1=H^2*sum w=H^2;
# W_i= h_i²/(H² w_i), so q_i=(h_i/W_i)/H1=w_i/h_i.
L=S.factor(dp+dq)
print('dlog(p_i*q_i) =',L)
print('at BQ=1:',S.factor(L.subs(Q,1/B)))
print('at BQ=-1:',S.factor(L.subs(Q,-1/B)))
F=S.symbols('F')
V=Q-2*z*(C*Q-B*E)+3*z**2*(C**2*Q-2*C*B*E+B**2*F)
X=E-2*z*(C*E-B*F)
f=(1+z*B**2*X-z*B**2*V*a)/(1+z*C-z*B*a)
f2=S.expand(S.series(f,z,0,3).removeO().coeff(z,2)).subs(Q,1/B).factor()
print('f2 on BQ=1:',S.collect(S.expand(f2),a))
# znew/z to first order at BQ=1: B^2 V^2 / average f^2
zrate=S.factor((-4*B*(C*Q-B*E)-2*(B**2*E-C)).subs(Q,1/B))
print('znew/z first-order at BQ=1:',zrate)
