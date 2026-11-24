from sage.all import *
import pickle,json,time
from pathlib import Path
par=json.loads(Path('workspace/agent4_allrational_params.json').read_text());co=json.loads(Path('workspace/agent4_allrational_coeffs.json').read_text());S=PolynomialRing(QQ,'t');t=S.gen();F=S.fraction_field();PX=PolynomialRing(F,'x');x=PX.gen();p=sum(QQ(a)*x**(3-i)for i,a in enumerate(co['pc']));q=sum(QQ(a)*x**(3-i)for i,a in enumerate(co['qc']));h=QQ(par['h']);left=QQ(par['L']);right=QQ(par['R']);eta=QQ(par['eta']);chi6=p*q-h;chi5,rem=chi6.quo_rem(x-eta);assert rem==0
red=lambda f:PX(f)%chi5
L=lambda f:red(q*(x-t)*f)[4]
H=matrix(F,3,3,lambda i,j:L(x**(i+j)));Hp=matrix(F,3,3,lambda i,j:L(p*p*x**(i+j))/h);Z=matrix(F,3,3,lambda i,j:red(p*x**i)[j+2]);Zinv=Z.inverse();cv=[];start=time.time()
for j in range(3):
 a=x**j;dc=vector(F,[0,0]+list(-Zinv*H.column(j)));nu=lambda f:sum(dc[i]*red(f)[i]for i in range(5));E=L(a*(p-q));nup=lambda f:(nu(p*p*f)+2*L(p*a*f)+E*L(p*p*f)/h)/h;b=-Hp.inverse()*vector(F,[nup(q*x**i)for i in range(3)]);Rc=q*a+p*sum(b[i]*x**i for i in range(3))+E;ci=2*q(t)/h*red(Rc)[4];assert ci.derivative()==0;cv.append(ci)
c=vector(F,cv);bb=h/(4*q(t))*H.inverse()*vector(F,[1,t,t*t]);B=bb.column()*c.row();assert B.trace()==(q(t).derivative()/q(t)-p(t).derivative()/p(t))/2;C=H.det()/p(t);assert C.derivative()==0
print('Exactc,trace,Christoffeldeterminantverifiedin',time.time()-start,'seconds');print('c approx',c.change_ring(RDF));print('C',C)
with open('workspace/agent2_rational_transport_setup.pkl','wb')as f:pickle.dump((S,PX,p,q,h,left,right,eta,chi5,chi6,H,c,C,bb),f)
