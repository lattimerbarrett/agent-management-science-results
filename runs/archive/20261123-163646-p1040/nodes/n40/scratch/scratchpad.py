import sympy as S
s=S.symbols('s'); t=1+s
D=S.diag(1,t); A=S.Matrix([[1,s],[0,1]])
def comm(a,b): return (a*b*a.inv()*b.inv()).applyfunc(S.cancel)
for c in range(3,8):
 Bk=S.Matrix([[1,0],[-s**(c-2),1]])
 z=comm(A,Bk)
 d=1+s**(c-1); a=s; b=-s**(c-2)
 factor=S.Matrix([[1,-a*a*b/d],[0,1]])*S.diag(1/d,d)*S.Matrix([[1,0],[a*b*b/d,1]])
 assert all(S.cancel(v)==0 for v in z-factor)
 print('c=',c,'opposite-root factorization verified; torus parameter =',d)
