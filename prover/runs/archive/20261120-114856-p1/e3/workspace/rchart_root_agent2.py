import sys,numpy as np
sys.path.insert(0,'workspace')
from generic_slow_agent3 import GenericSlow
from scipy.optimize import root
from scipy.integrate import solve_ivp
import mpmath as mp
mp.mp.dps=70
# alternating mirror q and qprime, pair negativeextras asymmetrically
H=.5;a=1;b=-.75;c=-1;d=-.75
xs=[float(mp.sqrt((5+2*mp.sqrt(2))/4)),float(mp.sqrt((5-2*mp.sqrt(2))/4))]
G=GenericSlow(a,b,c,d,H,-xs[0],xs[1]);G.setenergy(c,d,H)
lo,hi=-1.15891862259789,-.84108137740211
rng=np.random.default_rng(22)
for i in range(80):
 guess=[rng.uniform(lo,hi),rng.normal(),rng.uniform(-5,5),rng.uniform(.01,.99)]
 so=root(lambda y:G.extrarhs(0,y),guess,tol=1e-7)
 if so.success and np.linalg.norm(G.extrarhs(0,so.x))<1e-4 and lo<so.x[0]<hi and 0<so.x[3]<1:
  print('FIX',so.x,G.extrarhsfull(so.x),flush=True)
  break
else:print('no fixed',flush=True)
from pathlib import Path
Path('workspace/rchart_root_agent2.py').write_text(Path(__file__).read_text())
