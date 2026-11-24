from sage.all import *
import pickle
from pathlib import Path
with open('workspace/agent3_n7_jet5.pkl','rb') as f:D=pickle.load(f)
R=D['R'];zs=R.gens();G=D['G'];base=vector(QQ,D['base'][1:]);N=matrix(QQ,6,6,lambda i,j:G[i].polynomial().monomial_coefficient(zs[j].polynomial()))-identity_matrix(QQ,6)
S=PolynomialRing(QQ,'x');x=S.gen();beta=QQ(1)/100;chi=(x*x-1)**2*(x*x-beta)-beta;p=(x*x-1)*(x-QQ(1)/10);q=(x*x-1)*(x+QQ(1)/10);r=x*x-QQ(1)/2
co=lambda f: (f%chi)[5]
import sympy as sy
xx=sy.symbols('x');pinvs=sy.invert(sy.sympify(str(p).replace('^','**')),sy.sympify(str(chi).replace('^','**')),xx)
pinv=S(str(pinvs).replace('**','^'))
Tu=vector(QQ,[co(q*x*x**j) for j in range(1,7)]);Tv=vector(QQ,[co(q*x**j) for j in range(1,7)])
Ka=vector(QQ,[-co(q*r*((x-QQ(1)/10)*x)*pinv*x**j) for j in range(1,7)]);Kb=vector(QQ,[-co(q*r*(x-QQ(1)/10)*pinv*x**j) for j in range(1,7)])
v=-base;e1=N*v;e0=N*e1
B=matrix(QQ,[e0,Tu,Ka,Kb,e1,v]).transpose();print('rank',B.rank());assert B.is_invertible()
print('Jordan N=',B.inverse()*N*B)
for k in [0,1,2,3]:assert N*B.column(k)==0
with open('workspace/agent3_n7_normal_basis.pkl','wb') as f:pickle.dump(dict(B=B,Binv=B.inverse(),e0=e0,e1=e1,T=Tu,Ka=Ka,Kb=Kb,v=v),f)
