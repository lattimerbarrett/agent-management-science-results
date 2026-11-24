import pickle,sympy as S
D=pickle.load(open('workspace/agent4_nonmax_normal_jet.pkl','rb'))
x=D['x'];w=D['w0'];p=D['q'];q=D['Q'];C=D['C'];V=D['V'];n=len(x)
hc=S.Matrix(D['hvars']);h=V*hc
had=lambda *vs:S.Matrix([S.prod(v[i] for v in vs) for i in range(n)])
Dp=S.Matrix([S.prod(x[i]-x[j] for j in range(n) if i!=j) for i in range(n)])
A=(V.T*V).inv()*V.T*S.diag(*[Dp[i]*p[i]/C for i in range(n)])
f=A*w
v=D['b1'];u=had(w,p,h);du=had(v,p,h)
M=V.T*S.diag(*w)*V;dM=V.T*S.diag(*v)*V
ca=-M.inv()*V.T*had(u,p); a=V*ca
cad=-M.inv()*(V.T*had(du,p)+dM*ca);ad=V*cad
norm=(u.T*had(p,p))[0];dnorm=(du.T*had(p,p))[0]
z=had(w,p,p)/C;dz=had(v,p,p)/C
z1=(had(u,p,p)+2*had(w,p,a)-z*norm)/C
z1d=(had(du,p,p)+2*had(v,p,a)+2*had(w,p,ad)-dz*norm-z*dnorm)/C
N=V.T*S.diag(*z)*V;dN=V.T*S.diag(*dz)*V
cb=-N.inv()*V.T*had(z1,q);b=V*cb
cbd=-N.inv()*(V.T*had(z1d,q)+dN*cb);bd=V*cbd
nn=(z1.T*had(q,q))[0];dnn=(z1d.T*had(q,q))[0]
Bdir=(had(z1d,q,q)+2*had(dz,q,b)+2*had(z,q,bd)-v*nn-w*dnn)/C-du
Bmat=D['b1'].jacobian(hc)
acc=(Bdir+Bmat*D['hflow']).applyfunc(S.expand)
fd=A*v;fdd=A*acc
t=S.symbols('t');poly=lambda cs:sum(cs[i]*t**i for i in range(len(cs)))
fp=poly(f);fdp=poly(fd);fddp=poly(fdd)
P=S.interpolate(list(zip(x,p)),t);Q=S.interpolate(list(zip(x,q)),t);Delta=S.prod(t-i for i in x)
r=S.sqrt(-f[1]);ts=[-r,S.Integer(0),r]
val=lambda g,a:S.cancel(g.subs(t,a))
vel=[S.simplify(-val(fdp,a)/val(S.diff(fp,t),a)) for a in ts]
rootacc=[S.simplify(-(val(fddp,a)+2*val(S.diff(fdp,t),a)*vel[j]+val(S.diff(fp,t,2),a)*vel[j]**2)/val(S.diff(fp,t),a)) for j,a in enumerate(ts)]
for j,a in enumerate(ts):
 selfc=val(S.diff(Delta,t)/Delta-(S.diff(fp,t,2)/S.diff(fp,t)+S.diff(P,t)/P+S.diff(Q,t)/Q)/2,a)
 pred=selfc*vel[j]**2
 for k,b in enumerate(ts):
  if j==k:continue
  cab=val(S.diff(fp,t),b)*val(Delta,a)*(val(P,a)*val(Q,b)+val(Q,a)*val(P,b))/(2*val(S.diff(fp,t),a)*val(Delta,b)*val(P,a)*val(Q,a)*(a-b))
  pred+=cab*vel[k]**2
 assert S.expand(rootacc[j]-pred)==0
print('Generic normal-direction root acceleration formula exactly verified at rational nonmaximal quartic cycle.')
