import numpy as np
from scipy.optimize import differential_evolution, minimize
from math import sqrt
# symmetric finite hierarchies: top k cross red p, subgraph given recursively
# internal type: at each level equal k partition cross probability p, leaf all blue

def vals(params,ks):
    d=0.;A=0.;B=1.;has_red=False
    for p,k in reversed(list(zip(params,ks))):
        candidates=[0.]
        if has_red:candidates.append((A+(k-1)*p*p)/k)
        if p>0:candidates.append(((k-2)*p*p+2*p*d)/k)
        A=max(candidates)
        has_red=has_red or p>0
        B=(B+(k-1)*(1-p)**2)/k
        d=(d+(k-1)*p)/k
    return d,A,B

for alpha in [.17,.18,.19,.2,.205,.21,.22,.24]:
    base=max(2,(1+sqrt(alpha))**2,1+2*alpha/3+4*sqrt(alpha*(3-2*alpha))/3)
    best=(base,None)
    for ks in [[i,j] for i in range(2,9) for j in range(2,9)]+[[i,j,k] for i in [2,3,4] for j in [2,3,4] for k in [2,3,4]]:
        def obj(z):
            d,a,b=vals(z,ks)
            return b+100*max(0,a-alpha*b)
        result=differential_evolution(obj,[(0,1)]*len(ks),popsize=8,maxiter=250,tol=1e-8,polish=True)
        d,a,b=vals(result.x,ks)
        if a<=alpha*b+1e-7 and 1/b>best[0]+1e-6:
            best=(1/b,(ks,result.x,a,b,d))
            print('new best',alpha,best,flush=True)
    print('final',alpha,best,flush=True)
