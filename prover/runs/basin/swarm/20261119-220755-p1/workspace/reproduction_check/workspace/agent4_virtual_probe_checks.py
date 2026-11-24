"""Exact symbolic general-probe identity + rational Rayleigh examples."""
import sympy as s
z,c,th,N,A,C,v,Pz,Pt=s.symbols('z c th N A C v Pz Pt',nonzero=True)
F=N+Pz*(z-c);R=C*Pz-N*v/2*(1-Pz/Pt)/(z-th)
L=(R+A)/F-A/N-v/(2*(th-z))
rhs=Pz/F*(C-A*(z-c)/N+v/(2*(z-th))*((z-c)+N/Pt))
assert s.cancel(L-rhs)==0
B,K,S=s.symbols('B K S',nonzero=True);vv=-2*Pt*K/(N*S);Ctop=-(B+c*A)/N-vv/2
I=-(c*A+B)+S*K/(th-c)
res=s.factor(I-N*Ctop-N**2*vv/(2*(c-th)*Pt));assert s.cancel(res.subs(S**2,N+Pt*(th-c)))==0
print('General probe identity and canonical I formula: exact PASS')
x=s.Symbol('x');nodes=list(map(s.Rational,[-3,-1,1,2,3]))
f=x**3-7*x+5;theta=s.Rational(3,2);base=[]
for a in nodes:
 d=s.prod(a-b for b in nodes if b!=a);base.append(11*(a-theta)/(d*f.subs(x,a)))
assert sum(base)==1 and min(base)>0
nodes += [s.Rational(1,2),s.Rational(5,2)];p=[a*(1-s.Rational(3,10**6)) for a in base]+[s.Rational(1,10**6),s.Rational(2,10**6)]
d=[s.prod(a-b for b in nodes if b!=a) for a in nodes]
def op(p):
 V=s.Matrix([[a**j for j in range(3)] for a in nodes]);M=V.T*s.diag(*p)*V
 cc=M.inv()*(-V.T*s.Matrix([p[i]*a**3 for i,a in enumerate(nodes)]))
 f=x**3+sum(cc[j]*x**j for j in range(3));fv=[f.subs(x,a) for a in nodes]
 norm=sum(p[i]*fv[i]**2 for i in range(7));new=[p[i]*fv[i]**2/norm for i in range(7)]
 H=s.Poly(s.interpolate([(nodes[i],d[i]*p[i]*fv[i]/norm) for i in range(7)],x),x)
 assert H.degree()==3 and H.LC()==1
 return f,norm,new,H
probes=[s.Rational(-21,10),s.Rational(-9,10)];eta=[s.Rational(1)]*2;alphas=[[],[]]
for k in range(4):
 fk,norm,pp,H=op(p)
 for j,zz in enumerate(probes):
  # Certify the virtual root is below every original dual root by exact Sturm isolation.
  intervals=H.intervals(eps=s.Rational(1,10**20))
  assert len(intervals)==3 and all(pair[0][0]>zz for pair in intervals)
  alpha=-s.prod(zz-a for a in nodes)*eta[j]*fk.subs(x,zz)/(norm*H.eval(zz))
  alphas[j].append(alpha);eta[j]*=fk.subs(x,zz)**2/norm
 p=pp
for zz,aa in zip(probes,alphas):
 sign=s.sign(aa[0]);assert all(s.sign(a)==sign for a in aa)
 for k in range(2):assert aa[k+2]<=aa[k+1]**2/aa[k]
 ratios=[aa[k+1]/aa[k] for k in range(3)]
 assert all(sign*(ratios[k]-ratios[k+1])>=0 for k in range(2))
 print('probe',zz,'signed alpha',sign,'exact triple inequalities PASS')
print('ALL virtual probe finite checks PASSED')
