import sympy as S
s=S.symbols('s')
D=S.diag(1+s,1)
A=S.Matrix([[1,0],[s,1]])
B=S.Matrix([[1,-s],[0,1]])
def comm(a,b):return (a*b*a.inv()*b.inv()).applyfunc(S.cancel)
for c in range(3,9):
 bk=B
 for _ in range(c-3):bk=comm(D,bk)
 assert bk==S.Matrix([[1,-s**(c-2)],[0,1]])
 a=s;b=-s**(c-2);d=1-a*b
 gauss=S.Matrix([[1,-a*a*b/d],[0,1]])*S.diag(1/d,d)*S.Matrix([[1,0],[a*b*b/d,1]])
 assert all(S.cancel(x)==0 for x in comm(A,bk)-gauss[::-1,::-1]) if False else True
 # A is lower-root and B_k upper-root: conjugate the displayed Gauss identity by the coordinate swap.
 swap=S.Matrix([[0,1],[1,0]])
 assert all(S.cancel(x)==0 for x in comm(A,bk)-swap*gauss*swap)
 print('c =',c,': exact root and Gauss identities verified; pivot =',d)
