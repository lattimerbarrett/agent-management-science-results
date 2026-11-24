import sympy as s
e=s.symbols('e', integer=True, nonnegative=True)
def dot(D,F):
    a,b=D;c,d=F
    return s.expand(-e*a*c+a*d+b*c)
def add(D,F):return tuple(s.expand(x+y) for x,y in zip(D,F))
def scale(k,D):return tuple(s.expand(k*x) for x in D)
S=(1,0); f=(0,1); H=(1,3*e+1); P=add(scale(4,H),scale(-1,f));K=(-2,-e-2)
A=(5,-1);B=(-1,12*e+5); C=add(A,B)
c2=dot(A,B); h2=dot(H,H)
assert C==scale(4,H)
assert s.expand(c2-(65*e+26))==0
assert s.expand(dot(C,C)-c2-3*h2)==0
mu=dot(C,P)/2
assert s.expand(dot(A,P)-mu)==-3
assert s.expand(dot(B,P)-mu)==3
assert s.expand(dot(A,H)-dot(B,H))==0
chi=s.expand(2+(dot(C,C)-dot(C,K))/2-c2)
assert chi==-15*e
print('H^2 =',h2,'; c1^2 =',dot(C,C),'; c2 =',c2)
print('c1^2-c2 =',s.expand(dot(C,C)-c2),'; discriminant =',s.expand(4*c2-dot(C,C)))
print('P slopes:',dot(A,P),mu,dot(B,P),'; chi(E) =',chi)
# Cohomology of line bundles on F_e, by pushforward and Serre duality.
def h0(a,b,ev):
    if a<0:return 0
    return sum(max(b-i*ev+1,0) for i in range(a+1))
def h012(a,b,ev):
    h_0=h0(a,b,ev)
    h_2=h0(-2-a,-ev-2-b,ev)
    chi=(a+1)*(b+1)-ev*a*(a+1)//2
    return h_0,h_0+h_2-chi,h_2
for ev in range(8):
    ca=h012(5,-1,ev); cb=h012(-1,12*ev+5,ev)
    assert ca[0]+cb[0]==0
    assert ca[2]+cb[2]==0
    assert ca[1]+cb[1]==15*ev
    # End E0 obstruction vanishing
    assert h012(6,-12*ev-6,ev)[2]==0
    assert h012(-6,12*ev+6,ev)[2]==0
    # Sym powers times det: at least one H1 summand for arbitrarily large k.
    for k in range(6,25):
        a=5*k+4;b=-k+12*ev+4
        assert h012(a,b,ev)[1]>0
print('Line-bundle cohomology and obstruction checks passed for e=0,...,7; k=6,...,24.')
