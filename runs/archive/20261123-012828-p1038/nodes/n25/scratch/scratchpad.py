import sympy as s
T=s.symbols('T')
x,y=s.symbols('x y', positive=True)
# Widely separated rings, m=a=b=1, with positive row scalings.
# Rows are ordered: lower axis, upper axis, lower ring, upper ring.
P=[1-x*T,T**2*(-1+y*T),T+x,T**2*(1+T/y)]
M=s.Matrix([[s.expand(p).coeff(T,j) for j in range(4)] for p in P])
print('Widely separated limiting determinant:',s.factor(M.det()))
# In general, the one-ring limits have bidiagonal axial rows.
# Their final-row expansion has strictly positive coefficients.
u0,u1,a0,a1,a2=s.symbols('u0 u1 a0 a1 a2',positive=True)
K=s.Matrix([[1,-u0,0],[0,1,-u1],[a0,a1,a2]])
print('Typical limiting section determinant:',s.expand(K.det()))
