import sympy as s
u,v,w=s.symbols('u v w', real=True)
S=u+v+w
print('complement-partition total:',s.simplify(((1-u)+(1-v)+(1-w))/2))
print('excess after complement if original total < 1:',s.simplify(((1-u)+(1-v)+(1-w))/2-1))
# Cyclic diagonal symmetrization of a 3-part partition:
D=[[u,v,w],[v,w,u],[w,u,v]]
print('normalized quasitrace of each cyclic block:',[s.simplify(sum(row)/3) for row in D])
print('column totals:',[s.simplify(sum(D[i][j] for i in range(3))) for j in range(3)])
print('after k scalar refinements: uniform value S/(3*k), which tends to zero')
