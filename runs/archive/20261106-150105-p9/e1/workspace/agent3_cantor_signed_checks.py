import sympy as s, numpy as np, mpmath as mp, json
p,K,tau=s.symbols('p K tau',positive=True)
q=p/(p-1); dA=tau/K; dB=tau/K**(1/(p-1)); lam=K**(-1/p)
assert s.simplify(s.expand_power_base(lam/dA/dB,force=True)*tau**2/K**(1+1/(p-1)-1/p))==1
assert s.Rational(7,80)-s.Rational(2,100)>=s.Rational(1,16)
m,n,a,b,r=s.symbols('m n a b r',positive=True)
assert s.simplify(a*m+b*n-(a+b)*n-a*(m-n))==0
assert s.simplify(a*m+b*n-(a+b)*m-b*(n-m))==0

rng=np.random.default_rng(388)
r=.25; g=.5

def staircase(x,T):
 x=np.asarray(x,dtype=float).copy();out=np.zeros_like(x);scale=np.ones_like(x);alive=np.ones(x.shape,dtype=bool)
 for depth in range(65):
  left=alive&(x<r);right=alive&(x>1-r);gap=alive&~left&~right
  out[gap]+=scale[gap]*(T-(2*T-1)*(x[gap]-r)/g);alive[gap]=False
  out[right]+=scale[right]*(1-T);scale[left|right]*=T
  x[left]/=r;x[right]=(x[right]-(1-r))/r
  if not np.any(alive):break
 return out

def shell_samples(depth,exponent,N):
 offsets=np.zeros(N)
 for j in range(depth):offsets+=(1-r)*r**j*rng.integers(0,2,N)
 dist=(g/2)*rng.random(N)**(1/(1-exponent));z=np.where(rng.random(N)<.5,dist,g-dist)
 return offsets+r**depth*(r+z)

samples=[]
for T in [.501,.52,.55]:
 for M,N in [(0,0),(0,5),(3,2),(7,9)]:
  x=r*shell_samples(M,.49,20000); y=(1-r)+r*shell_samples(N,.47,20000)
  tx=staircase(x,T);ty=staircase(y,T)
  mean=float(np.mean((ty-tx)/(y-x)))
  assert mean>2-3*T
  # Pointwise negative quotient bound for bridge-versus-subtree.
  xx=r+g*rng.random(20000);yy=r*shell_samples(N,.48,20000)
  val=(staircase(xx,T)-staircase(yy,T))/(xx-yy)
  assert np.min(val)>=-(2*T-1)/g-1e-9
  samples.append({'T':T,'depthA':M,'depthB':N,'cross_average':mean,'proved_lower':2-3*T,'bridge_min':float(np.min(val)),'bridge_lower':-(2*T-1)/g})

mp.mp.dps=50
plateaus=[]
for pp in [mp.mpf('2.1'),mp.mpf(3),mp.mpf(5),mp.mpf(10)]:
 for KK in [mp.mpf(2),mp.mpf(10),mp.mpf(100),mp.mpf(1000)]:
  tt=mp.mpf('.01');qq=pp/(pp-1);dA=tt/KK;dB=tt/KK**(1/(pp-1));aa=dA/pp;bb=dB/qq
  eps=mp.expm1((aa+bb)*mp.log(4));L=int(mp.ceil(1/(aa*mp.log(4))));N0=int(mp.ceil(mp.log(2)/mp.log1p(eps)))
  assert eps<mp.mpf('.1')
  z=mp.exp(-aa*mp.log(4));tri=L/(1-z)-z*(1-z**L)/(1-z)**2
  assert tri>=mp.exp(-1)*L*(L+1)/2
  lower=KK**(-1/pp)*tri/(32*eps*L)
  simple=KK**(-1/pp)/(64*mp.e*eps*aa*mp.log(4))
  assert lower>=simple
  alpha=1+1/(pp-1)-1/pp
  plateaus.append({'p':float(pp),'K':float(KK),'L':L,'N0':N0,'epsilon':float(eps),'lower_bound':float(lower),'normalized_by_K_alpha':float(lower/KK**alpha)})
print('Symbolic identities and constants verified; 12 signed kernel sampling checks passed.')
print(json.dumps(plateaus,indent=2))
with open('workspace/agent3_cantor_signed_checks.py','w') as f:f.write(open('scratchpad.py').read())
with open('workspace/agent3_cantor_signed_checks.json','w') as f:json.dump({'samples':samples,'plateaus':plateaus},f,indent=2)
