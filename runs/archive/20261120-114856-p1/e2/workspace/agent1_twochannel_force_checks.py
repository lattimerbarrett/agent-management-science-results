from sage.all import *
import pickle,time
Z=PolynomialRing(QQ,'z');z=Z.gen();K=NumberField(z**4-18*z*z+25,'k');k=K.gen();a=(k*k-5)/(2*k);b=(k*k+5)/(2*k);assert a*a==2 and b*b==7
FT=FunctionField(K,'th');th=FT.gen();RX=PolynomialRing(FT,'x');x=RX.gen();chi=x**6-14*x**4+49*x*x-36;full=(chi.quo_rem(x+2)[0])*x*(x-b);assert full.degree()==7
p=x**3-7*x+3*a;q=x**3-7*x-3*a;r=(x+2)*(x-th)
def L(num,f):return ((num*f)%chi)[5]
def jac(num,poly):
 H=matrix(FT,3,3,lambda i,j:L(num,x**(i+j)));Hi=H.inverse();hh=L(num,poly*poly);momout=[L(num,poly*poly*x**j)/hh for j in range(1,7)]
 rows=[]
 for j in range(1,7):
  def dL(f):return (f%full)[j]
  dpvec=-Hi*vector(FT,[dL(poly*x**i) for i in range(3)]);dp=sum(dpvec[i]*x**i for i in range(3));dh=dL(poly*poly)
  rows.append(vector(FT,[(dL(x**i*poly*poly)+2*L(num,x**i*poly*dp)-momout[i-1]*dh)/hh for i in range(1,7)]))
 return matrix(rows).transpose()
start=time.time();J=jac(q*r,p);J1=jac(p*r,q);print('jac time',time.time()-start)
N=J1*J-identity_matrix(FT,6);NN=N*N;assert N*N*N==zero_matrix(FT,6)
forces=[]
for xi in (FT(0),FT(b)):
 inj=vector(FT,[xi**j-3**j for j in range(1,7)])
 force=-(NN*inj)[0];forces.append(force)
 print('force xi',xi,':',force.factor())
ratio=-forces[1]/forces[0];print('ratio',ratio.factor());print('ratio derivative',ratio.derivative().factor())
kk=-16*(th+b)*(th-3)*(th-2)*(th-1)*(th+1)*(th+3)/((th**3-7*th)**2-18)
assert forces[0]==kk*(th-b) and forces[1]==kk*th
assert ratio==th/(b-th) and ratio.derivative()==b/(b-th)**2
assert (p*q-18)==chi
assert L(q*r,1)==1 and L(q*r,x)==2-th
for j in range(3):assert L(q*r,p*x**j)==0
print('Exact two-channel force and restoring-ratio assertions passed.')
