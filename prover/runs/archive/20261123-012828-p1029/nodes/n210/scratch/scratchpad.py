import sympy as s
# Finite block-row identity behind a legitimate matrix amplification.
x1,x2,x3=s.symbols('x1 x2 x3',commutative=False)
y1,y2,y3=s.symbols('y1 y2 y3',commutative=False) # formal adjoints
T=s.Matrix([[x1,x2,x3]])
Tstar=s.Matrix([[y1],[y2],[y3]])
print('TT* =',T*Tstar)
print('T*T =',Tstar*T)
print('diagonal pinching of T*T =',s.diag(y1*x1,y2*x2,y3*x3))
print('For x_i=sqrt(b_i), TT*=sum b_i and diag(T*T)=diag(b_i).')
print('q_3(T*T)=q(sum b_i) is valid for a compatible finite amplification.')
print('q_3(T*T)=sum q(b_i) would additionally require pinching invariance.')
print('Neither infinite amplification nor continuity of an extension follows from the stated axioms.')
print('RETRACTION: the previous assertion of quasitracial exhaustion was false.')
