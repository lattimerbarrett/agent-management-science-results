import sympy as S
z,B,C,Q,E,F,a=S.symbols('z B C Q E F a', nonzero=True)
# Four core nodes (s=3), or generally s+1 core nodes.
# h_i=L_i(0), l_i=L_i(beta), a_i=l_i/h_i.
# B=sum h_i*l_i/w_i, C=sum l_i^2/w_i,
# Q=sum a_i*w_i, E=sum a_i^2*w_i, F=sum a_i^3*w_i.
# In projective coordinates, exact two-block core multipliers are
# f_i=(1+z*B^2*(X-V*a_i))/(1+z*C-z*B*a_i),
# V=sum a_i*w_i/(1+z*C-z*B*a_i)^2,
# X=sum a_i^2*w_i/(1+z*C-z*B*a_i)^2.
V=Q-2*z*(C*Q-B*E)+3*z*z*(C*C*Q-2*C*B*E+B*B*F)
X=E-2*z*(C*E-B*F)
f=(1+z*B*B*(X-V*a))/(1+z*C-z*B*a)
fseries=S.series(f,z,0,3).removeO().expand()
first=S.factor(fseries.coeff(z,1))
print('First-order core multiplier:',first)
print('Its a-dependent coefficient:',S.factor(S.diff(first,a)))
print('At positive neutrality B*Q=1:',S.factor(first.subs(Q,1/B)))
second=S.factor(fseries.coeff(z,2).subs(Q,1/B))
print('Second order at positive neutrality:',S.collect(S.expand(second),a))
# Normalized core weights remove any multiplier independent of a_i.
# Therefore their first-order displacement is
# 2 z B (1-BQ) w_i (a_i-Q).
assert S.simplify(S.diff(first,a)-B*(1-B*Q))==0
assert S.simplify(S.diff(first.subs(Q,1/B),a))==0
print('Verified: first-order tangential displacement vanishes at positive neutrality.')
