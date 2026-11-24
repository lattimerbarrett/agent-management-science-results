import sympy as sp
I=sp.eye(2)
P=[sp.Matrix([[1,0],[0,0]]),sp.Matrix([[1,1],[1,1]])/2,sp.Matrix([[1,-2],[-2,4]])/5]
C=sp.Rational(2)
e=sp.Rational(1,8)
def psd(A):
    assert A==A.T
    assert A[0,0]>=0 and A[1,1]>=0 and A.det()>=0
for p in P:
    assert p*p==p and p.T==p
psd(C*I-sum(P,sp.zeros(2)))
T=I
D=[]
for p in P:
    D.append(p*T)
    T=(I-e*p)*T
assert sum((d.T*d for d in D),sp.zeros(2))==(I-T.T*T)/(2*e-e*e)
assert T-I==-e*sum((p*d for p,d in zip(P,D)),sp.zeros(2))
psd(e*C/(2-e)*I-(T-I).T*(T-I))
print('Exact rational product identities and uniform norm bound passed.')
print('T =',T)
print('bound squared =',e*C/(2-e))
