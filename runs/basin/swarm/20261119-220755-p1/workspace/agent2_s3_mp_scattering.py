import mpmath as mp
from fractions import Fraction
from sage.all import QQ,PolynomialRing,AA,RealField

def effective(qc=-2,L=11,ix=(0,3,4),nodes=(-3,-1,1,2,3),dps=90,left_index=3,right_index=4):
 mp.mp.dps=dps;RR=RealField(int(dps*3.5)+20)
 def cv(a):return mp.mpf(str(RR(a)))
 PR=PolynomialRing(QQ,'x');x=PR.gen();PP=PR.prod if False else None;P=1
 for a in nodes:P*=x-QQ(a)
 Qc=QQ(str(Fraction(str(qc))));NN=QQ(str(Fraction(str(L))));poly=P*(x-Qc);roots=(poly+NN).roots(AA,multiplicities=False);neg=(poly+2*NN).roots(AA,multiplicities=False)
 if len(roots)!=6 or len(neg)!=6:return None
 zz=[cv(roots[i]) for i in ix];ee=[cv(roots[i]) for i in range(6) if i not in ix];mu,nu=cv(neg[left_index]),cv(neg[right_index]);N=cv(NN);c=cv(Qc);a,b=map(mp.mpf,nodes[2:4])
 f=lambda z:mp.fprod(z-v for v in zz);g=lambda z:mp.fprod(z-v for v in ee);fp=lambda j:mp.fprod(zz[j]-zz[k] for k in range(3) if k!=j);cr=mp.matrix([(zz[j]-c)*g(zz[j])/fp(j) for j in range(3)]).T;Ra=g(a)/f(a)
 # Split quadrature at geometric boundary layers, including both root distances.
 ds=min([abs(v-a) for v in zz+ee]+[abs(v-b) for v in zz+ee]);nn=max(3,int(mp.ceil(-mp.log10(ds/(b-a))))+2);pts={a,b,(a+b)/2}
 for k in range(1,nn+1):pts.add(a+(b-a)*mp.power(10,-k));pts.add(b-(b-a)*mp.power(10,-k))
 pts=sorted(pts);r=mp.matrix([mp.quad(lambda th:-1/(2*mp.sqrt(Ra)*(z-c)*(z-th)**2*mp.sqrt(g(th)/f(th))),pts) for z in zz]);T=mp.eye(3)+r*cr
 def F(z,th):return mp.matrix([-4*f(z)**2/((z-v)*(v-c)*(v-th)) for v in zz])
 def E(z,th):return mp.matrix([-4*f(z)/(N*(z-th)*(z-c))*cr[0,j]*(zz[j]-th)/(z-zz[j]) for j in range(3)]).T
 F0,F1=F(mu,a),mp.lu_solve(T,F(nu,b));L0,L1=E(mu,a),E(nu,b)*T;C=mp.matrix([[ (L0*F0)[0],(L0*F1)[0] ],[(L1*F0)[0],(L1*F1)[0]]]);k=C[0,1]*C[1,0]/(C[0,0]*C[1,1]);err=(cr*r)[0]-(mp.sqrt((g(b)/f(b))/Ra)-1)
 return dict(C=C,k=k,quadcheck=err,roots=zz,groot=ee,mu=mu,nu=nu,T=T)
