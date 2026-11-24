import sympy as S
s=S.symbols('s'); t=1+s
# Audit the claimed column Alexander matrices and determinant balancing.
D=S.diag(t,1,1)
A=S.eye(3); A[1,0]=s
B=S.eye(3); B[0,1]=-s
C=S.eye(3); C[2,1]=s

def balance(M): return S.diag(M,1/S.det(M))
def simp(M): return M.applyfunc(S.cancel)
for M,N in [(D,A),(A,B),(D,C),(A*C,B*D)]:
 assert simp(balance(M*N)-balance(M)*balance(N))==S.zeros(4)
print('Determinant balancing IS a homomorphism for the audited noncommuting higher-rank matrices.')

def comm(M,N):return simp(M*N*M.inv()*N.inv())
W=comm(D,comm(A,B))
assert W!=S.eye(3)
print('The balanced degree-three word has the claimed base matrix: ', simp(balance(W)-comm(balance(D),comm(balance(A),balance(B))))==S.zeros(4))
print('These checks prove neither a lift to the claimed nilpotent quotient nor survival of its central subgroup.')
