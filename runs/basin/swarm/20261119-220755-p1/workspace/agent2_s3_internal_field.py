import sympy as s
from pathlib import Path
Path('workspace/agent2_s3_internal_field.py').write_text(Path('scratchpad.py').read_text())
x,T,A,B,C=s.symbols('x T A B C');nodes=list(map(s.Integer,[-3,-1,1,2,3]));P=s.prod(x-z for z in nodes);d=[s.diff(P,x).subs(x,z) for z in nodes]
f0=x**3-7*x+5;g0=x**3-7*x-5;u=-A/10+B*(x*x-2*x-3)/10+C*x

def coeff(p):return s.Matrix([s.expand(p).coeff(x,j) for j in range(3)])
def pfrom(c):return x**3+sum(c[j]*x**j for j in range(3))
def mf(weights):
 m=[s.factor(sum(p*z**j for z,p in zip(nodes,weights))) for j in range(6)]
 return s.Matrix(3,3,lambda i,j:m[i+j]),-s.Matrix(m[3:6])
def weights(poly):return [s.cancel(poly.subs(x,z)/di) for z,di in zip(nodes,d)]
M0,r0=mf(weights((x-T)*f0));M1,r1=mf(weights((x-T)*u));MI=M0.inv().applyfunc(s.factor)
g1=(MI*(r1-M1*coeff(g0))).applyfunc(s.factor);g2=(-MI*M1*g1).applyfunc(s.factor)
gp1=sum(g1[j]*x**j for j in range(3));gp2=sum(g2[j]*x**j for j in range(3))
# Remainder gives N' and H'.
R0=s.rem((x-T)*f0*g0,P,x);R1=s.rem((x-T)*(u*g0+f0*gp1),P,x);R2=s.rem((x-T)*(u*gp1+f0*gp2),P,x)
n0=s.expand(R0).coeff(x,1);n1=s.expand(R1).coeff(x,1);n2=s.expand(R2).coeff(x,1)
z0=s.expand(R0).coeff(x,0);z1=s.expand(R1).coeff(x,0);z2=s.expand(R2).coeff(x,0)
t1=s.factor(-z1/n0+z0*n1/n0**2);t2=s.factor(-z2/n0+z1*n1/n0**2-z0*n1**2/n0**3+z0*n2/n0**2)
print('single theta velocity',t1)
W0=weights((x-T)*g0);W1=weights((x-T)*gp1-t1*g0);W2=weights((x-T)*gp2-t1*gp1-t2*g0)
MM0,rr0=mf(W0);MM1,rr1=mf(W1);MM2,rr2=mf(W2);MMI=MM0.inv().applyfunc(s.factor)
h1=(MMI*(rr1-MM1*coeff(f0))).applyfunc(s.factor);print('h1-u',[s.factor(h1[j]-coeff(u)[j]) for j in range(3)])
h2=(MMI*(rr2-MM1*h1-MM2*coeff(f0))).applyfunc(s.factor)
# h2 = -Adot/10+Bdot*(x²−2x−3)/10+Cdot*x.
Bdot=s.factor(10*h2[2]);Adot=s.factor(-10*h2[0]-3*Bdot);Cdot=s.factor(h2[1]+Bdot/5)
RR1=s.rem((x-T)*(gp1*f0+g0*u)-t1*g0*f0,P,x);nn1=s.expand(RR1).coeff(x,1);zz1=s.expand(RR1).coeff(x,0);theta_dot=s.factor(-zz1/11-T*nn1/11)
print('theta_dot',theta_dot);print('Adot',Adot);print('Bdot',Bdot);print('Cdot',Cdot)
Path('workspace/agent2_s3_internal_field.txt').write_text(str({'theta':theta_dot,'A':Adot,'B':Bdot,'C':Cdot}))
