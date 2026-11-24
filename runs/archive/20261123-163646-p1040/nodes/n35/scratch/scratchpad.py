import sympy as S
s=S.symbols('s'); t=1+s
# Coordinate order (x3,x1), so A is the upper root.
D=S.diag(1,t)
A=S.Matrix([[1,s],[0,1]])
B=S.Matrix([[1,0],[-s,1]])
def simp(M): return M.applyfunc(S.factor)
def comm(X,Y): return simp(X*Y*X.inv()*Y.inv())
Bk=B
for c in range(3,9):
    assert Bk==S.Matrix([[1,-s**(c-2)],[0,1]])
    H=comm(A,Bk)
    a=s; b=-s**(c-2); d=1-a*b
    X=S.Matrix([[1,-a*a*b/d],[0,1]])
    T=S.diag(1/d,d)
    Y=S.Matrix([[1,0],[a*b*b/d,1]])
    assert simp(H-X*T*Y)==S.zeros(2)
    # Extension fixing additional free generators pads these blocks by identities.
    for n in (3,4,6):
        pad=lambda M:S.diag(M,S.eye(n-3)) if n>3 else M
        Db=S.diag(pad(D),1/t)
        Hb=S.diag(pad(H),1)
        Wb=comm(Db,Hb)
        assert Wb==S.diag(comm(D,H),S.eye(n-2))
    print('degree',c,': exact root/torus decomposition and stabilization verified; torus parameter',d)
    Bk=comm(D,Bk)
