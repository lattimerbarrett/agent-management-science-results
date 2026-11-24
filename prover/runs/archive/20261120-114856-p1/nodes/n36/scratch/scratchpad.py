import numpy as np
from scipy.special import logsumexp
rng=np.random.default_rng(81)
# Search for weight-sensitive scalar quantities, in addition to the standard
# monic-polynomial norm. Two-step changes are essential for cycle invariants.
def update(lam,w,s):
    prev=np.zeros(len(w));v=np.ones(len(w));hp=1.
    for j in range(s):
        hh=w@(v*v);a=w@(lam*v*v)/hh
        vn=(lam-a)*v-(hh/hp)*prev if j else (lam-a)*v
        prev,v,hp=v,vn,hh
    h=w@(v*v)
    return w*v*v/h,h
counts={k:[0,0] for k in ['entropy','mean','Stieltjes(-1)','log potential(-1)','Kantorovich(-1)']}
for rep in range(250):
    lam=np.sort(rng.uniform(.1,5,6));w=rng.dirichlet(np.ones(6));s=2
    wp,h=update(lam,w,s);wpp,hp=update(lam,wp,s)
    for name,fun in [('entropy',lambda v:-sum(v*np.log(v))),('mean',lambda v:v@lam),('Stieltjes(-1)',lambda v:v@(1/(lam+1))),('log potential(-1)',lambda v:v@np.log(lam+1)),('Kantorovich(-1)',lambda v:(v@(lam+1))*(v@(1/(lam+1))))]:
        d=fun(wpp)-fun(w)
        counts[name][0]+=d>1e-12;counts[name][1]+=d< -1e-12
    assert hp>=h-1e-10
print('Candidate two-step changes [positive, negative]:',counts)
# Exhibit the unresolved-by-h feature: four-node stationary cycle fibers
# carry distinct Stieltjes transforms although p,q and their norm are fixed.
h=.1
levels=(-11+np.array([-1,1])*np.sqrt(1+4*h))/2
lam=np.sort(np.concatenate([(5+np.array([-1,1])*np.sqrt(25+4*c))/2 for c in levels]))
p=lambda x:x*x-5*x+5
q=lambda x:x*x-5*x+6
pd=np.prod(np.where(np.eye(4,dtype=bool),1,lam[:,None]-lam[None,:]),axis=1)
print('Fixed-cycle core',lam)
for xi in np.linspace(lam[1]+.1*(lam[2]-lam[1]),lam[2]-.1*(lam[2]-lam[1]),3):
    w=q(lam)*(lam-xi)/pd;w/=sum(w)
    assert min(w)>0
    wp,H=update(lam,w,2);wpp,Hp=update(lam,wp,2)
    print('free root',xi,'h',H,'Stieltjes(-1)',w@(1/(lam+1)),'return error',max(abs(wpp-w)))
