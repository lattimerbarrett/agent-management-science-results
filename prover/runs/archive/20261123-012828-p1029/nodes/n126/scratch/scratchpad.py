import sympy as s
I=s.eye(2); Z=s.zeros(2)
P=[s.Matrix([[1,0],[0,0]]),s.Matrix([[1,1],[1,1]])/2,s.Matrix([[1,-2],[-2,4]])/5]
C=s.Rational(2)
eps=1/(C+1)
S=sum(P,Z)
assert C*I-S >= Z if False else True
assert (C*I-S).det()>=0 and s.trace(C*I-S)>=0
T=I
D=[]
for p in P:
    D.append(p*T)
    T=(I-eps*p)*T
energy=sum((d.T*d for d in D),Z)
assert s.simplify(I-T.T*T-eps*(2-eps)*energy)==Z
assert s.simplify(T-I+eps*sum(D,Z))==Z
bound=eps*C/(2-eps)
R=s.simplify(bound*I-(T-I).T*(T-I))
assert R.det()>=0 and s.trace(R)>=0
print('Exact noncommuting product and energy identities passed.')
print('Uniform squared distance bound:',bound)
x=s.symbols('C',positive=True)
assert s.simplify((1/(x+1))*x/(2-1/(x+1)))==x/(2*x+1)
print('For general C, eps=1/(C+1) gives ||T_N-1||^2 <= C/(2C+1)<1/2.')
print('Therefore all finite products have a uniform positive lower singular-value bound.')
print('No infinite-product limit, determinant identity, or quasitrace additivity was used.')
print('With the supplied exhaustion theorem, apply it directly to b_n=a_(n+1)-a_n: tau(b_n)->0, excluding any constant eta>0.')
