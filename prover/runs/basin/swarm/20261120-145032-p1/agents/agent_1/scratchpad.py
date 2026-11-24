import numpy as np
from scipy.optimize._numdiff import approx_derivative
a=.5;v=.3;vp=1+a*a-v;f=(v-a*a)*(1-v)
tlo=(v+vp-np.sqrt((v-vp)**2-4*f))/2;thi=(v+vp+np.sqrt((v-vp)**2-4*f))/2
roots=np.array([-np.sqrt(thi),-np.sqrt(tlo),np.sqrt(tlo),np.sqrt(thi)])
l=np.r_[[-1.,-a,a,1.],roots]
powers=np.array([l**j for j in range(5)])
def F(w):
 w=np.atleast_2d(w);m=w@powers.T
 c=(m[:,3]-m[:,1]*m[:,2])/(m[:,2]-m[:,1]**2);d=m[:,2]-c*m[:,1]
 q=powers[2]-c[:,None]*l-d[:,None];z=w*q*q;return z/z.sum(axis=1)[:,None]
def G(w):return F(F(w))[0]
p=(v-a*a)/(1-a*a);base=np.r_[[p/2,(1-p)/2,(1-p)/2,p/2],np.zeros(4)]
Bmat=np.vstack([np.eye(7),-np.ones(7)]) # use different derivative direct directional tangent
J=approx_derivative(lambda z:G(base+np.r_[z,-sum(z)]),np.zeros(7))
# J maps tangent coords to output8; N outputs full8: subtract tangent input
Bmat=np.vstack([np.eye(7),-np.ones(7)]);N=J-Bmat
for i,root in enumerate(roots):
 direction=-base.copy();direction[i+4]+=1
 g=J@direction[:7]-direction
 acc=N@g[:7]
 print(root,'g',np.round(g,5),'acc',np.round(acc,5))
