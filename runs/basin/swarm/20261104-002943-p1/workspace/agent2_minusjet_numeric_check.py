import sys,numpy as np
sys.path.insert(0,'workspace');import agent2_twominus_ode as m
h=np.array([.2,.3,-.1,.05]);A=np.array([.07,.09]);u=m.w0*m.p*(m.V@h);w2=np.r_[np.zeros(m.na),A*A]-sum(A*A)*m.w0
out=m.weightjet(m.weightjet([m.w0,u,w2,np.zeros(m.n)],m.p),m.q)
def F(w):
 M=m.V.T@(w[:,None]*m.V);c=np.linalg.solve(M,-m.V.T@(w*m.x**4));p=m.x**4+m.V@c
 return w*p*p/np.dot(w,p*p)
errs=[]
for t in [.1,.05,.025,.0125]:
 actual=F(F(m.w0+t*u+t*t*w2));approx=sum(t**j*out[j] for j in range(4));e=np.linalg.norm(actual-approx);errs.append(e);print(t,e)
ratios=np.array(errs[:-1])/errs[1:]
assert np.all((ratios>15)&(ratios<17))
print('ratios',ratios)
