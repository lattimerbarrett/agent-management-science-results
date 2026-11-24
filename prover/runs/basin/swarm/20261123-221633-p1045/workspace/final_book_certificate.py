import sympy as S
u,s,D=S.symbols('u s D',positive=True)
h=S.symbols('h1:4',nonnegative=True);m=S.symbols('m1:4',nonnegative=True)
r=S.sqrt(3);a=u*u;t=2*r*u;kap=3-(2*r-3)/u;lam=4/t-2;K=3-t;star=4/r-2;c0=3-(r-1)/u
li=[4/(t+kap*z)-2 for z in h]
H=sum(h);M=sum(m)
P=sum(kap**2*h[i]**2/(3*(t+kap*h[i]))+4*kap*h[i]*m[i]/(t*(t+kap*h[i])) for i in range(3))
f=1+2*a-4*u/r;g=(1-u)**2
lower=(1-s)*K-kap*s*(a-s)-a*sum(li)+sum(li[i]*m[i] for i in range(3))+3*s-2*D+H
E=lam*(H+2*M)/2-2*D+c0*H+3*u*s
assert S.factor(lower-3*f-E-3*u*(star-u)*s-kap*s*s+P)==0
assert S.simplify(g-f-u*(star-u))==0
assert S.simplify(1+kap/3-lam/2-c0)==0
lo=1/(2*r);hi=S.Rational(1,3)
assert S.simplify(kap.subs(u,lo)-S.Rational(4,3))>0
assert S.simplify(S.Rational(5,3)-kap.subs(u,hi))>0
assert 2-2/r-S.Rational(5,27)>0
assert S.simplify(c0.subs(u,lo))>0
k=lam/2
J=3*u-1/k+S.Rational(18,25)*(c0-S.Rational(1,4))
assert S.simplify(S.diff(J,u,2)+6/(1-r*u)**3+S.Rational(36,25)*(r-1)/u**3)==0
Jlo=S.simplify(J.subs(u,lo));Jhi=S.simplify(J.subs(u,hi))
assert S.simplify(Jlo-(97*r-167)/50)==0
assert S.simplify(Jhi-(232-133*r)/50)==0
assert Jlo>0 and Jhi>0
Q=S.symbols('Q',real=True)
assert S.Rational(108,205)>S.Rational(18,25)**2
F=Q/4-S.Rational(205,729)*Q*Q+S.Rational(4,27)
assert S.diff(F,Q,2)<0
assert F.subs(Q,S.Rational(18,25))==S.Rational(1231,6750)>0
assert F.subs(Q,S.Rational(11,9))==S.Rational(7943,236196)>0
assert (S.Rational(25,27)+2*S.Rational(10,3))/3==S.Rational(205,81)
v=S.symbols('v',real=True)
B=S.Rational(1,2)+v*v*(S.Rational(1,2)+v*v-2*v)-(1-v)**2
assert S.simplify(B-(v*v-1)*(2*v*v-4*v+1)/2)==0
al=S.symbols('al',positive=True)
c3=1+2*al/3+4*S.sqrt(al*(3-2*al))/3
astar=S.simplify(star**2);bstar=S.simplify((1-star)**2);alstar=S.simplify(astar/bstar)
assert S.simplify(alstar-(52-16*r)/121)==0
assert S.simplify(c3.subs(al,S.Rational(1,6))-2)==0
assert S.simplify(c3.subs(al,alstar)-(1+S.sqrt(alstar))**2)==0
x,y,L=S.symbols('x y L')
page=1+(1-x)**2+(1-y)**2+L*x*y-(3-4/(2+L))
sos=(2+L)/4*(x+y-4/(2+L))**2+(2-L)/4*(x-y)**2
assert S.factor(page-sos)==0
for ks in [2,3,4]:
    z=S.symbols('z:'+str(ks));Z=sum(z);rr=L*(ks-1)/2
    lhs=sum((1-v)**2 for v in z)+L*sum(z[i]*z[j] for i in range(ks) for j in range(i))
    rhs=ks*rr/(1+rr)+(1-L/2)*sum((v-Z/ks)**2 for v in z)+(1+rr)/ks*(Z-ks/(1+rr))**2
    assert S.factor(lhs-rhs)==0
z=S.symbols('z',positive=True)
ct=(S.sqrt(3-2*z*z)+2*z)**2/3
pt=3*z/(S.sqrt(3-2*z*z)+2*z)
assert S.simplify(ct*pt**2/3-z*z)==0
assert S.simplify(ct*(1+2*(1-pt)**2)/3-1)==0
pr=z/(1+z);cr=(1+z)**2
assert S.simplify(cr*pr**2-z*z)==0
assert S.simplify(cr*(1-pr)**2-1)==0
assert S.factor((1+2*(1-x)**2)-(2*(1-x)+(1-x)**2))==x*x
print('ALL EXACT SYMBOLIC IDENTITIES AND SIGNS PASSED')
print('alpha* =',alstar,'=',S.N(alstar,16))
import random, math
N=600;alpha=.2;n=500;rng=random.Random(8675309)
p=3*math.sqrt(alpha)/(math.sqrt(3-2*alpha)+2*math.sqrt(alpha))
rows=[0]*N
for i in range(N):
    for j in range(i+1,N):
        if i%3!=j%3 and rng.random()<p:
            rows[i]|=1<<j;rows[j]|=1<<i
mask=(1<<N)-1
blue=[mask^rows[i]^(1<<i) for i in range(N)]
maxbooks=[]
for color in (rows,blue):
    largest=0
    for i in range(N):
        edges=color[i]&~((1<<(i+1))-1)
        while edges:
            bit=edges&-edges;j=bit.bit_length()-1
            largest=max(largest,(color[i]&color[j]).bit_count())
            edges-=bit
    maxbooks.append(largest)
assert maxbooks[0]<math.ceil(alpha*n) and maxbooks[1]<n
print('Exhaustive finite-book check:',N,maxbooks,'forbidden',math.ceil(alpha*n),n)
print('ALL SYMBOLIC AND FINITE CHECKS PASSED')
