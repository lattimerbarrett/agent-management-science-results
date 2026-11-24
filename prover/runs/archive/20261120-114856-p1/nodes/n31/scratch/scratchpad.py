import numpy as np
from scipy.special import logsumexp
from pathlib import Path
rng=np.random.default_rng(42)
h=.1
levels=(-7+np.array([-1,1])*np.sqrt(1+4*h))/2
zcore=np.sort(np.concatenate([(5+np.array([-1,1])*np.sqrt(25+4*c))/2 for c in levels]))
core=np.sort(np.r_[-np.sqrt(zcore),np.sqrt(zcore)])
neglev=(-7+np.array([-1,1])*np.sqrt(1-4*h))/2
znegs=np.sort(np.concatenate([(5+np.array([-1,1])*np.sqrt(25+4*c))/2 for c in neglev]))
# Two symmetric outside modes in one negative-level gap.
xi=np.sqrt(znegs[0]);nodes=np.r_[core,-xi,xi]
q=lambda t:t**4-5*t*t+4
p=lambda t:t**4-5*t*t+3
pd=np.prod(np.where(np.eye(8,dtype=bool),1,core[:,None]-core[None,:]),axis=1)

def step(lw):
    w=np.exp(lw-logsumexp(lw));prev=np.zeros(len(w));v=np.ones(len(w));hp=1.
    for j in range(4):
        hh=np.dot(w,v*v);a=np.dot(w,nodes*v*v)/hh
        vnew=(nodes-a)*v-(hh/hp)*prev if j else (nodes-a)*v
        prev,v,hp=v,vnew,hh
    norm=np.dot(w,v*v)
    new=lw+2*np.log(np.maximum(abs(v),1e-300));new-=logsumexp(new)
    return new,norm,v

print('symmetric core:',core,'outside:',[-xi,xi],flush=True)
print('max exact-target core product error',max(abs(p(core)*q(core)-h)),flush=True)
records=[]
for trial in range(16):
    roots=np.array([rng.uniform(core[1],core[2]),rng.uniform(core[3],core[4]),rng.uniform(core[5],core[6])])
    hc=np.prod(core[:,None]-roots,axis=1)
    wc=q(core)*hc/pd;wc/=wc.sum()
    assert min(wc)>0
    eps=10**rng.uniform(-9,-5)
    wc*=np.exp(rng.normal(size=8)*eps**.5)
    lw=np.log(np.r_[wc,eps*rng.uniform(.1,1),eps*rng.uniform(.1,1)])
    saved=[];hs=[]
    for k in range(16000):
        lw,H,v=step(lw)
        if k%2000==1999:saved.append(np.exp(lw));hs.append(H)
    changes=[np.linalg.norm(saved[i+1]-saved[i]) for i in range(len(saved)-1)]
    print(trial,'h',hs[-1],'late distance',changes[-3:],'active',np.sum(saved[-1]>1e-8),flush=True)
    records.append(dict(roots=roots,eps=eps,weights=saved,hs=hs,loglast=lw))
np.save('s4_symmetric_scan.npy',records,allow_pickle=True)
