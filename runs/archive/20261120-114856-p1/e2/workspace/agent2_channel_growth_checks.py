from sage.all import *
import pickle,time
P=PolynomialRing(QQ,'z');z=P.gen();K=NumberField(z**4-18*z**2+25,'s',embedding=AA(2).sqrt()+AA(7).sqrt());s=K.gen();aa=(s-5/s)/2;bb=(s+5/s)/2
S=PolynomialRing(K,'t');t=S.gen();F=S.fraction_field();th=F(t);L=list(map(F,[-3,-1,1,2,3]));ext=[F(0),F(bb)];d=3*aa;h=F(18);p=lambda x:x**3-7*x+d;q=lambda x:x**3-7*x-d
X=matrix(F,[[1,x,x*x]for x in L]);Xe=matrix(F,[[1,x,x*x]for x in ext]);db=[1/prod(L[i]-L[j]for j in range(5)if j!=i)for i in range(5)];w=vector(F,[di*q(x)*(x-th)for di,x in zip(db,L)]);H=X.T*diagonal_matrix(w)*X
Z=matrix(F,[[1]*5]+[[p(x)*x**j for x in L]for j in range(3)]+[[0,0,0,0,1]]);Zinv=Z.inverse();w1=vector(F,[wi*p(x)**2/h for wi,x in zip(w,L)]);H1=X.T*diagonal_matrix(w1)*X
rows=[]
for j in range(3):
 a=vector(F,[int(i==j)for i in range(3)]);aL=X*a;dw=Zinv*vector(F,[0]+list(-H*a)+[0]);E=sum(w[i]*aL[i]*(p(L[i])-q(L[i]))for i in range(5));dw1=vector(F,[(dw[i]*p(L[i])**2+2*w[i]*p(L[i])*aL[i]+w1[i]*E)/h for i in range(5)]);b=-H1.inverse()*X.T*vector(F,[dw1[i]*q(L[i])for i in range(5)]);Re=vector(F,[q(x)*sum(a[j]*x**j for j in range(3))+p(x)*sum(b[j]*x**j for j in range(3))+E for x in ext]);rows.append(vector(F,[(4*E-2*r)/h for r in Re]))
D=matrix(F,rows).T;V=4*H.inverse()*Xe.T*diagonal_matrix([p(x)for x in ext]);M=D*V
print('Matrix entries factored:')
for i in range(2):
 for j in range(2):
  v=M[i,j];print(i,j,'NUM',v.numerator().factor(),'DEN',v.denominator().factor(),flush=True)
for i in [0,1]:
 num=M[i,i].numerator();deg=num.degree();SX=PolynomialRing(K,'y');yy=SX.gen();bern=SX(sum(num[k]*(1+2*yy)**k*(1+yy)**(deg-k)for k in range(deg+1)))
 print('Diagonal',i,'positiveBernstein coefficients?',all(AA(c)>0 for c in bern.list()),'coeffs',bern.list(),flush=True)
 assert all(AA(c)>0 for c in bern.list())
assert M[0,1]==M[1,0]
print('detM=',M.det().numerator().factor(),'/',M.det().denominator().factor(),flush=True)
num=M.det().numerator();deg=num.degree();bern=SX(sum(num[k]*(1+2*yy)**k*(1+yy)**(deg-k)for k in range(deg+1)))
assert all(AA(c)>0 for c in bern.list())
print('det positive Bernstein certified')
with open('workspace/agent2_channel_growth_matrix.pkl','wb')as f:pickle.dump((K,S,M),f)
