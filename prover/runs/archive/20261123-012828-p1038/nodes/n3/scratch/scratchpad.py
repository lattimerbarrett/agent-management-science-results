import sympy as s
x,y,h,d=s.symbols('x y h d', real=True)
w=x+s.I*y
D=d+h
# Stereographic map from north pole: (h,w)/d -> w/(d-h).
# Use d^2=h^2+x^2+y^2 to compare its value with the stated roots.
t_forward=D/s.conjugate(w)
t_reverse=-w/D
print('Forward stereographic-root discrepancy numerator:')
print(s.factor((t_forward-w/(d-h))*(d-h)*s.conjugate(w)))
print('Reverse stereographic-root discrepancy:',s.simplify(t_reverse-(-w)/(d+h)))
print('Antipodal identity:',s.simplify(t_reverse+1/s.conjugate(t_forward)))
print('Forward inverse stereographic height:')
# |D/conj(w)|^2=(d+h)/(d-h) on the distance relation.
u=(d+h)/(d-h)
print(s.simplify((u-1)/(u+1)))
