import numpy as np
# Exact two-dimensional eigenvalue/eigendirection formula for the kernel.
# W(x)=sum_i lam_i P_i, W(y)=sum_j mu_j Q_j.
# T=sum_ij (lam_i/mu_j)^(2/p) tr(P_i Q_j)
# D=(det(W(x))/det(W(y)))^(2/p)
# ||W(x)^(1/p)W(y)^(-1/p)||^2=(T+sqrt(T*T-4*D))/2.
for p in [1.5, 3., 5.]:
    for theta in [0.,.01,.3,1.]:
        lam=np.array([100.,1.]); mu=np.array([30.,2.])
        R=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        overlap=R**2
        T=np.sum((lam[:,None]/mu[None,:])**(2/p)*overlap)
        D=(np.prod(lam)/np.prod(mu))**(2/p)
        exact=np.sqrt((T+np.sqrt(max(0,T*T-4*D)))/2)
        M=np.diag(lam**(1/p))@R@np.diag(mu**(-1/p))@R.T
        numerical=np.linalg.norm(M,2)
        print('p',p,'theta',theta,'identity error',abs(exact-numerical),
              'Frobenius/op ratio',np.sqrt(T)/numerical)
# Discarding eigendirection overlaps can lose arbitrarily large powers:
# for W(x)=W(y)=diag(t,1), the exact kernel is 1,
# but the largest eigenvalue-ratio envelope is t^(1/p).
for t in [10.,1e3,1e6]:
    print('constant weight, p=3, t=',t,'exact kernel=1, eigenvalue-only envelope=',t**(1/3))
