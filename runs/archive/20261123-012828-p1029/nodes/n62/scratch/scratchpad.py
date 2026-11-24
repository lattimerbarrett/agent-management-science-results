import sympy as s
# Verify the compression identity using a symbolic self-adjoint 2x2 block.
a,b,c=s.symbols('a b c', real=True)
p=s.diag(1,0)
y=s.Matrix([[a,b],[b,c]])
print('p*y^2*p - (p*y*p)^2 =')
print(p*y*y*p-(p*y*p)**2)
print('p*y*(1-p)*y*p =')
print(p*y*(s.eye(2)-p)*y*p)
