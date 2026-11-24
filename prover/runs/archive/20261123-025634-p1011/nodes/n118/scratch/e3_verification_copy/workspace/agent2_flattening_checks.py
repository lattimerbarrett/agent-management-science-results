import sympy as s
for d in range(2,8):
 p=s.Matrix(s.symbols('p:'+str(d)))
 T=s.eye(d+1)
 for i in range(d):T[d,i]=p[i]
 G=T.T*T
 expected=s.eye(d+1)
 for i in range(d):expected[i,d]=expected[d,i]=-p[i]
 expected[d,d]=1+(p.T*p)[0]
 assert T.det()==1
 assert s.simplify(G*expected)==s.eye(d+1)
 print('exact vertical-graph metric identity dimension',d+1)
p=s.Matrix(s.symbols('p:3'));K=s.Matrix(3,3,lambda i,j:s.Symbol('K'+str(min(i,j))+str(max(i,j))))
W=s.sqrt(1+(p.T*p)[0])
Hmeasure=sum(W*s.diff(p[i]/W,p[j])*K[i,j] for i in range(3) for j in range(3))
assert s.simplify(Hmeasure-s.trace(K)+(p.T*K*p)[0]/(1+(p.T*p)[0]))==0
print('exact graph H dS cubic-remainder identity checked')
