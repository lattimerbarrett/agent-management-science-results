import sympy as s
import mpmath as mp
import numpy as np
import os
mp.mp.dps=60
X=s.symbols('X')
def exact_Q(N):
    alpha=s.Rational(N+2,2); beta=alpha-s.Rational(1,2)
    pol=[]
    for j in range(4):
        P=0
        for k in range(j+1):
            prod=s.prod(X-(alpha-q)**2 for q in range(1,k+1))
            den=s.factorial(k)*s.prod(beta-t for t in range(1,k+1))
            P+=(-1)**(j-k)*s.binomial(j,k)*prod/den
        pol.append(s.Poly(P,X))
    bases=[s.Poly(s.prod(X-(alpha-1-2*h)**2 for h in range(r)),X) for r in range(9)]
    sums=[s.simplify(4**r/(alpha-r-1)*(s.gamma(s.Rational(2*r+1,2))*s.gamma(s.Rational(1,2))/(s.gamma(alpha-r-s.Rational(1,2))*s.gamma(alpha-s.Rational(1,2)))+s.gamma(r+1)/(s.gamma(alpha-r)*s.gamma(alpha)))) for r in range(9)]
    Q=s.zeros(4)
    for i in range(4):
        for j in range(i,4):
            p=pol[i]*pol[j]*s.Poly((X-(alpha-1)**2)**2,X)
            val=0
            for r in reversed(range(p.degree()+1)):
                coeff=p.nth(r)
                val+=coeff*sums[r]
                p-=coeff*bases[r]
            assert p.is_zero
            Q[i,j]=Q[j,i]=s.simplify(val)
    return Q
for n in range(17,31):
    Q=exact_Q(n)
    q=np.array(Q.evalf(18)).astype(float)
    scale=np.sqrt(np.diag(q)); q=q/scale[:,None]/scale[None,:]
    M=q*np.add.outer(np.arange(4),np.arange(4))+q
    eig=np.linalg.eigvalsh(M)
    print(n,eig)
    if n in (18,19):
        with open('workspace/agent1_exact_Q_'+str(n)+'.txt','w') as f:f.write(str(Q))
