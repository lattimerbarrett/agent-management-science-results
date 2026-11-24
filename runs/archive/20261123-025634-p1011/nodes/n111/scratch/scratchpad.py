import sympy as s
# Flat ambient coordinates pulled back by T(y)=(y1,y2,y3,y4+h(y1,y2,y3)).
y=s.symbols('y1:5'); N=4
h=y[0]**2+2*y[1]**2+y[0]*y[2]**2+y[1]**4
T=s.Matrix([y[0],y[1],y[2],y[3]+h]); J=T.jacobian(y)
g=J.T*J; gi=g.inv()
Gamma=[[[s.simplify(sum(gi[k,l]*(s.diff(g[l,j],y[i])+s.diff(g[l,i],y[j])-s.diff(g[i,j],y[l])) for l in range(N))/2) for j in range(N)] for i in range(N)] for k in range(N)]
expected=all(s.simplify(Gamma[k][i][j]-(s.diff(h,y[i],y[j]) if k==N-1 and i<N-1 and j<N-1 else 0))==0 for k in range(N) for i in range(N) for j in range(N))
curv=[]
for k in range(N):
 for l in range(N):
  for i in range(N):
   for j in range(N):
    r=s.diff(Gamma[k][j][l],y[i])-s.diff(Gamma[k][i][l],y[j])+sum(Gamma[k][i][a]*Gamma[a][j][l]-Gamma[k][j][a]*Gamma[a][i][l] for a in range(N))
    if s.simplify(r)!=0:curv.append((k,l,i,j,s.simplify(r)))
Hess=s.hessian(h,y[:3]).subs(dict.fromkeys(y,0))
# Domain above graph: outward normal points down, so II at zero is Hess(h).
II0=Hess; IItracefree=II0-s.trace(II0)/3*s.eye(3)
print('Graph pullback Christoffels have only Gamma^n_ab = h_ab:',expected)
print('Number of nonzero ambient Riemann components:',len(curv))
print('Boundary II at origin:',II0)
print('Boundary trace-free II at origin:',IItracefree)
print('Conclusion: flat ambient metric permits a nonumbilic graph boundary; no such compatibility obstruction exists.')
