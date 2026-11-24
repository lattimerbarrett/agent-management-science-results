import numpy as np,itertools
from scipy.optimize import brentq
from scipy.integrate import quad

def canonical_kernel(nodes,c,N,roots,ix,mu,nu):
 a,b=nodes[2:4]; ff=roots[list(ix)]; gg=roots[[j for j in range(6)if j not in ix]]
 f=lambda z:np.prod(z-ff);g=lambda z:np.prod(z-gg)
 f2=-sum(ff);g2=-sum(gg);R=lambda z:g(z)/f(z);sqN=np.sqrt(N)
 J0=quad(lambda t:(np.sqrt(R(t))+1/np.sqrt(R(t)))/2,a,b,epsabs=1e-9,epsrel=1e-9,limit=200)[0]
 J1=quad(lambda t:((2*t+f2)*np.sqrt(R(t))+(2*t+g2)/np.sqrt(R(t)))/2,a,b,epsabs=1e-9,epsrel=1e-9,limit=200)[0]
 T=np.array([[1,0,-J0],[0,1,-J1],[0,0,1.]])
 def F(z,e):
  r=R(e);u=f(z)**2/N
  return 4*N*np.array([1+u,(1+u)*(z+e)+f2+u*g2,(1+r*u)/((z-e)*np.sqrt(r))])
 def L(z,e):return -4/(N*(z-c))*np.array([z,1,sqN/(z-e)])
 f0=F(mu,a);f1=np.array([[1,0,J0],[0,1,J1],[0,0,1.]])@F(nu,b)
 l0=L(mu,a);l1=L(nu,b)@T
 C=np.array([[l0@f0,l0@f1],[l1@f0,l1@f1]])
 return C,C[0,1]*C[1,0]/(C[0,0]*C[1,1]),(J0,J1)

if __name__=='__main__':
 rng=np.random.default_rng(938);best=0;tests=0;coops=0
 for it in range(300):
  nodes=np.sort(rng.uniform(-3,3,5))
  if min(np.diff(nodes))<.15:continue
  c=rng.uniform(nodes[0]+.05,nodes[2]-.05)
  if min(abs(nodes-c))<.05:continue
  rho=np.sort(np.r_[nodes,c]);prod=lambda x:np.prod(x-rho)
  xm=[brentq(lambda x:sum(1/(x-rho)),rho[j]+1e-12,rho[j+1]-1e-12)for j in [0,2,4]]
  N=rng.uniform(.01,.49)*min(-prod(z)for z in xm)
  if N<1e-5:continue
  def rr(level):
   ans=[]
   for j,m in zip([0,2,4],xm):
    ans.extend([brentq(lambda x:prod(x)+level,rho[j],m,xtol=1e-14),brentq(lambda x:prod(x)+level,m,rho[j+1],xtol=1e-14)])
   return np.array(ans)
  roots=rr(N);neg=rr(2*N);mu,nu=neg[3:5]
  for ix in itertools.product(*[(0,1),(2,3),(4,5)]):
   C,k,_=canonical_kernel(nodes,c,N,roots,ix,mu,nu);tests+=1
   if C[0,1]>0 and C[1,0]>0:
    coops+=1;best=max(k,best)
    assert k<1+1e-5,(nodes,c,N,ix,C,k)
 print('DONE tests',tests,'coop',coops,'maxk',best)
