import numpy as np
def reflected_moment(kappa, eps_squared, Q):
    m=.5+eps_squared
    d=np.sqrt(m*m-2*kappa*eps_squared)
    rp,rm=m+d,m-d
    den=(rp-kappa)*Q**rp+(kappa-rm)*Q**rm
    if den<=0:return np.inf
    return Q**(-kappa)*(rp-rm)*Q**(rp+rm)/den
if __name__=="__main__":
    for k in [.5,.75,.9,1,1.1]:
        print(k,[reflected_moment(k,.1,Q) for Q in [10,100,1000]])
