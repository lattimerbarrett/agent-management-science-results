"""Numerical checks of the weighted Taylor expansion used in the lifting theorem.
This does not certify a periodic orbit: it checks finite exact-map evaluations.
"""
import numpy as np,sys
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
D=np.load('workspace/agent2_rational_positive_eq_0.4.npz')
ob=BlowupODE(D['base'],D['f'],D['g'],D['N'],D['mus'])
s=ob.s;n=len(ob.nodes)
nodes=np.r_[ob.nodes,ob.mus]
V=np.array([nodes**j for j in range(s)]).T
def op(p,nod=nodes):
 VV=np.array([nod**j for j in range(s)]).T
 fc=np.linalg.solve(VV.T@(p[:,None]*VV),-VV.T@(p*nod**s))
 fv=nod**s+VV@fc;N=np.dot(p,fv**2)
 return fc,N,p*fv**2/N
Y=D['y'].copy();Y[0]+=1e-6;Y[1:s+1]+=1e-6*np.array([.02,-.01,.03,-.02]);Y[-2:]*=[1.000003,.999998]
field=ob(0,Y,True)
constants=[]
for eps in [.004,.002,.001,.0005]:
 f=ob.f.copy();f[:s]+=eps*Y[1:1+s]
 H=ob.nodes+Y[0]
 base=H/(ob.d*np.polynomial.polynomial.polyval(ob.nodes,f));base/=sum(base)
 ext=eps**2*Y[-2:];p=np.r_[base*(1-sum(ext)),ext]
 assert min(p)>0 and abs(sum(p)-1)<1e-13
 p2=op(op(p)[2])[2];b=p2[:n]/sum(p2[:n]);fc,N,_=op(b,ob.nodes)
 H2=ob.d*b*(ob.nodes**s+ob.V@fc)/N
 hc=np.mean(H2-ob.nodes)
 eps2=eps/(1+eps)
 Y2=np.r_[hc,(fc-ob.f[:s])/eps2,p2[n:]/eps2**2]
 rem=(Y2-Y-eps*field)/eps**2
 constants.append(np.linalg.norm(rem));print('epsilon',eps,'Taylor constant',constants[-1])
assert all(np.isfinite(constants)) and max(constants)<20
# Check a fully explicit unstable radial lifting by backwards Green iteration.
# tau advances with epsilon; delta_next=(1+alpha*epsilon)*delta+epsilon^2*sin(tau).
K=1000;M=200000;alpha=.7
k=np.arange(M+1);eps=1/(k+K);tau=np.r_[0,np.cumsum(eps[:-1])]
delta=np.zeros(M+1)
for j in range(M-1,-1,-1):
 delta[j]=(delta[j+1]-eps[j]**2*np.sin(tau[j]))/(1+alpha*eps[j])
err=delta[1:]-(1+alpha*eps[:-1])*delta[:-1]-eps[:-1]**2*np.sin(tau[:-1])
assert max(abs(err))<1e-17
assert min(1+delta)>0
assert max(abs(delta/eps))<2
print('Backwards hyperbolic lifting recurrence residual',max(abs(err)))
print('All finite checks passed; periodic-orbit existence remains separate.')
