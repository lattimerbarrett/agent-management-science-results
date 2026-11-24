"""Exact algebra checks for the elementary mixed-triangle proof.
Requires only SymPy; no floating-point arithmetic is used.
"""
import sympy as S
Q=S.Rational
h=S.sqrt(3)
p,r,m,y,z,t=S.symbols('p r m y z t',real=True)
a=p*p/3;s=1-r
g3=4*p/3-2*p*p/3;gh=2*p/h-p*p/3
nu=1+(h-2)/p
U=2*a*(1-p)/p+2*p*s/3+r*p/h+nu*r*(a-r)/s
assert S.simplify(U-(g3+r*(gh-g3)-nu*(1-a)*r*r/s))==0
# Theta-cap radical inequality.
H=2*p-1;E=1-2*p/3;B=1-8*p/3+2*p*p;D=1-2*p+2*p*p/3
assert S.simplify((S.sqrt(E)-H)**2-2*(B+D)-2*H*((3-p)/3-S.sqrt(E)))==0
assert S.expand(E-D-g3)==0
assert S.expand((1-p/3)**2-E-p*p/9)==0
# Exact T_x and perpendicular C eigenvalue identities.
x0,x1,L=S.symbols('x0 x1 L',real=True);x=S.Matrix([x0,x1,1-x0-x1])
e2=x[0]*x[1]+x[0]*x[2]+x[1]*x[2];d2=1-3*e2
T=S.Matrix([[x[0],x[2],x[1]],[x[2],x[1],x[0]],[x[1],x[0],x[2]]])
assert S.factor(T.charpoly().as_expr().subs(T.charpoly().gen,L)-(L-1)*(L*L-d2))==0
nu0=h-1+(h-2)*t
M=S.eye(3)/3+nu0*S.diag(*x)+t*(T-S.diag(*x))
e=S.ones(3,1)/h;delta=x-S.ones(3,1)/3
assert S.simplify(M*e-(1+t)/h*e-(nu0-t)/h*delta)==S.zeros(3,1)
P=S.Matrix([[1/S.sqrt(2),1/S.sqrt(6)],[-1/S.sqrt(2),1/S.sqrt(6)],[0,-2/S.sqrt(6)]])
C=S.simplify(P.T*M*P);C0=(1+nu0-t)/3;K=2*t+nu0
assert S.simplify(S.trace(C)-2*C0)==0
assert S.simplify(C.det()-(C0*C0-K*K*d2/9))==0
low=((h-1)+(2*h-3)*t-(h-1)/t)/3
assert S.simplify(low-(C0-K*(1/t-1)/3))==0
assert S.simplify(low.subs(t,h/2)-1/(6*h))==0
assert S.simplify(low.subs(t,h-1)-(7-4*h)/3)==0
# Rational bounds used in the two Schur-complement cases.
checks=[h-1>Q(18,25),1/(6*h)>Q(9,100),(7-4*h)/3>Q(1,50),
        (4-2*h)**2<Q(29,100),(h-1)**2/4<Q(7,50),
        Q(2,3)*(2/h-1)**2<Q(2,125),(2-h)/3<Q(9,100),
        Q(29,100)*Q(2,125)/(3*Q(9,100))<Q(1,50),
        Q(7,50)*Q(9,100)/(3*Q(1,50))==Q(21,100),
        Q(29,100)/(9*Q(9,100)*Q(49,50))<Q(2,5),
        Q(7,50)/(9*Q(1,50)*Q(79,100))<1]
assert all(bool(v) for v in checks)
# Far-partition convexity and endpoint identities.
assert S.expand((4+3*p)**3-324*p-(3*p-2)**2*(3*p+16))==0
J=(2*a+r*(a-r)/s)/(3*m)+m*(s*(5-3*m)+3*r)/(3*(1+m))
A0=2*a+r*(a-r)/s;K0=8-5*r
assert S.simplify(S.diff(J,m,2)-Q(2,3)*(A0/m**3-K0/(1+m)**3))==0
P0=y*y*(y**4-12*y**3+46*y*y-60*y+25)+y*z*(y**4-18*y**3+100*y*y-126*y+43)+z*z*(-6*y**3+58*y*y-58*y+22)
P1=y*y*(2*y*y-20*y+50)+y*z*(y*y-82*y+97)+z*z*(-3*y*y-102*y+45-36*z)
D0=12*(2-y)*(1-y)*(1+y)*(1-y-z)
D1=12*(1+y)*(4-2*y-3*z)
for mm,PP,DD in [(p/(3*(1-p)),P0,D0),(2*p/(3*s),P1,D1)]:
 diff=S.factor((g3-J.subs(m,mm)).subs(r,2*p-1+z).subs(p,(1+y)/2))
 assert S.factor(diff-PP/DD)==0
# Each grouped coefficient is positive on 0<=y,z<=1/9.
assert all(v>0 for v in [25-Q(60,9)-Q(12,9**3),43-Q(126,9)-Q(18,9**3),
                         22-Q(58,9)-Q(6,9**3),50-Q(20,9),97-Q(82,9),
                         45-Q(3,81)-Q(102,9)-Q(36,9)])
# Exact transition conversion.
a0=(4/h-2)**2;b0=(1-S.sqrt(a0))**2
astar=(52-16*h)/121
assert S.simplify(a0/b0-astar)==0
assert S.simplify((1+2*a0-4*S.sqrt(a0/3))-b0)==0
assert S.simplify((1+Q(2,3)*Q(1,6)+Q(4,3)*S.sqrt(Q(1,6)*(3-2*Q(1,6))))-2)==0
print('All exact mixed-triangle algebra, radical bounds, and transitions passed.')

# Construct actual finite colorings and compute EVERY edge's booksize.
import numpy as np
rng=np.random.default_rng(20260703)
alpha_star=float((52-16*h)/121)
for alpha in [0.1,1/6,0.18,alpha_star,0.25,0.5,1.0]:
    n=700;eps=0.7
    if alpha<=1/6:C=2.
    elif alpha<alpha_star:C=1+2*alpha/3+4*np.sqrt(alpha*(3-2*alpha))/3
    else:C=(1+np.sqrt(alpha))**2
    N=int(np.floor((C-eps)*n))
    if alpha<=1/6:
        A=np.zeros((N,N),dtype=np.int32);k=N//2
        A[:k,k:]=1;A[k:,:k]=1
    else:
        prob=np.sqrt(3*alpha/C) if alpha<alpha_star else np.sqrt(alpha)/(1+np.sqrt(alpha))
        A=np.triu((rng.random((N,N))<prob).astype(np.int32),1);A+=A.T
        if alpha<alpha_star:
            for I in np.array_split(np.arange(N),3):A[np.ix_(I,I)]=0
    Blue=np.ones((N,N),dtype=np.int32)-np.eye(N,dtype=np.int32)-A
    RR=A@A;BB=Blue@Blue
    red=int(RR[A==1].max(initial=0));blue=int(BB[Blue==1].max(initial=0))
    assert red<int(np.ceil(alpha*n)) and blue<n,(alpha,N,red,blue)
    print('finite check',alpha,N,red,blue)
