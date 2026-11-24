from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gammaln
sys.path.insert(0,'workspace')
from agent4_jet_matrix import block
n=19
for l in [2,3,4,8,20,40]:
    c=l*(l+n-1)-n
    theta0=1e-5
    h2=c/(2*l+n)
    def rhs(t,Y):
        return [Y[1],c*Y[0]-(2*l+n-1)/np.tan(t)*Y[1]]
    sol=solve_ivp(rhs,[theta0,np.pi/2],[1+h2*theta0**2/2,h2*theta0],rtol=3e-12,atol=1e-12)
    h,hp=sol.y[:,-1]
    mu_num=hp/h
    mu_gamma=2*np.exp(gammaln(l/2)+gammaln((l+n+1)/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
    err=abs(mu_num/mu_gamma-1)
    assert err<1e-9
    print('n,l,ODE DN,gamma DN,relative error:',n,l,mu_num,mu_gamma,err)
js,eigs,B=block(19,2,100000)
print('Independent reproduction, degrees',2+2*np.array(js),'eigenvalues',eigs)
assert eigs[0]<-0.00117
Path('workspace/agent2_independent_shape_check.py').write_text(Path(__file__).read_text())
