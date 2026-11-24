import sympy as s
I=s.eye(3)
A=s.Matrix([[-1,0],[0,1]])
B=s.Matrix([[-1,2],[0,1]])
C=s.Matrix([[1,0],[2,-1]])

def project(M):
    return s.Matrix([[M[0,0]-M[2,0],M[0,1]-M[2,1]],[M[1,0]-M[2,0],M[1,1]-M[2,1]]])

def K(i,j):
    M=I.copy();M[i,i]=-1;M[i,j]=2
    return M

def T(i,j,k):
    M=I.copy();M[i,j]=2;M[i,k]=-2
    return M

raw=[K(0,1),K(0,2),T(0,1,2),K(1,0),K(1,2),T(1,0,2),K(2,0),K(2,1),T(2,0,1)]
expected=[B,A,A*B,C,A,A*C,C,B,B*C]
for J,E in zip(raw,expected):
    assert J*s.ones(3,1)==s.ones(3,1)
    Q=project(J.inv())
    assert Q==E or Q==-E
for M in [A,B,C]:assert M*M==s.eye(2)
print("All nine Fox(-1) projective matrices checked exactly.")
