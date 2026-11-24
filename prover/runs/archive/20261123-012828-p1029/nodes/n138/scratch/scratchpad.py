import sympy as s
# Check the compression criterion p <= h iff p h^{-1} p <= p
# for p=diag(1,0), h a positive real symmetric 2x2 matrix.
a,b,c=s.symbols('a b c', real=True)
h=s.Matrix([[a,b],[b,c]])
p=s.diag(1,0)
print('det(h-p) =',s.factor((h-p).det()))
print('1-(h^-1)[0,0] =',s.factor(1-h.inv()[0,0]))
print('The numerators coincide; h>0 makes det(h)>0.')
