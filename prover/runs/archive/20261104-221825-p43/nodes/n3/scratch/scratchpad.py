import sympy as s
R = s.diag(-1, -1, 1)  # time-one rotation for H(x)=pi*x_3
print('Kernel of R-I:', (R-s.eye(3)).nullspace())
x1,x2,x3,y1,y2,y3=s.symbols('x1 x2 x3 y1 y2 y3', real=True)
solutions=s.solve([2*x1,2*x2,2*y1,2*y2,x1*x1+x2*x2+x3*x3-1,y1*y1+y2*y2+y3*y3-1], [x1,x2,x3,y1,y2,y3], dict=True)
print('Fixed points:', solutions)
print('Number of distinct fixed points:',len(solutions))