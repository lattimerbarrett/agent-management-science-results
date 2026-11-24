import sys,numpy as np
sys.path.insert(0,'workspace')
from agent2_reflected_moments import reflected_moment
rng=np.random.default_rng(202607)
N=30000;dt=.001;Q=10.;eps2=.1;L=np.log(Q)
x=np.full(N,L);loga=np.zeros(N);active=np.ones(N,dtype=bool)
for step in range(200000):
    ix=np.flatnonzero(active)
    if not len(ix):break
    dB=rng.normal(0,np.sqrt(dt),len(ix))
    x[ix]=np.minimum(L,x[ix]+dB-(.5+eps2)*dt)
    loga[ix]+=dB-.5*dt
    active[ix[x[ix]<=0]]=False
assert not active.any()
for k in [.5,.75]:
    samples=np.exp(k*loga)
    estimate=samples.mean();se=samples.std(ddof=1)/np.sqrt(N)
    exact=reflected_moment(k,eps2,Q)
    print('k=',k,'MonteCarlo=',estimate,'SE=',se,'ODE=',exact,'z=',(estimate-exact)/se)
    assert abs(estimate-exact)<=5*se+.01
print('Reflected diffusion: all',N,'paths absorbed; steps=',step)
from pathlib import Path
Path('workspace/agent2_reflected_montecarlo.py').write_text(Path(__file__).read_text())
