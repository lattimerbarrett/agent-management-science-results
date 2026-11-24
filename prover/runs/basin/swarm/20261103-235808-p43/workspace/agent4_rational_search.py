import sympy as S,numpy as np
from pathlib import Path
w,u,z,c,d,e=S.symbols('w u z c d e',real=True)
Q=1+c*(z-1)**2+d*(z-1)**3+e*(z-1)**4
p=2*w/(1+w*w);uu=(w*w-1)/(1+w*w);zz=2*(p+uu/S.sqrt(2))**2
Fp=S.Poly(S.cancel((uu*Q.subs(z,zz)-(2-3*uu**2))*(1+w*w)**9).expand(),w)
Fm=S.Poly(S.expand(u*Q.subs(z,2-u*u)+(2-u*u)),u)
cp=S.lambdify((c,d,e),Fp.all_coeffs(),'numpy');cm=S.lambdify((c,d,e),Fm.all_coeffs(),'numpy')
rng=np.random.default_rng(123)
best=99;counts={}
for j in range(100000):
 vals=[-5/16,*rng.uniform(-100,100,2)]
 rp=np.roots(np.asarray(cp(*vals),float));rm=np.roots(np.asarray(cm(*vals),float))
 goodm=[r.real for r in rm if abs(r.imag)<1e-6 and -1+1e-5<r.real<1-1e-5]
 if goodm:continue
 goodp=[r.real for r in rp if abs(r.imag)<1e-5 and abs(r.real)>1e-4]
 counts[len(goodp)]=counts.get(len(goodp),0)+1
 if len(goodp)<best:
  best=len(goodp);print('best',best,vals,goodp)
 if len(goodp)==1:
  print('FOUND',vals,'roots+',goodp,'roots-',rm);break
else:print('none')
Path('workspace/agent4_rational_search.py').write_text(Path('scratchpad.py').read_text())