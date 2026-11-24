from pathlib import Path
code=Path('workspace/agent2_fz.py').read_text().split('cols=parts(12)')[0].replace('D=12','D=13')
ns={};exec(code,ns)
for n in range(len(ns['BAp']),17): ns['BAp'].append(ns['conv'](ns['BAp'][-1],ns['BA']))
sigs=[s for n in range(16) for s in ns['parts'](n) if all(j%3!=2 for j in s)]
F48={s:ns['f'](s).copy() for s in sigs}
ns['k0']=47;ns['f'].cache_clear();ns['block'].cache_clear()
F47={s:ns['f'](s).copy() for s in sigs}
import math
for sig in sigs:
 m=sig.count(1); out={}
 for k in range(m+1):
  rem=sig[k:];c=math.comb(m,k)*math.factorial(k)
  for mon,v in F47[rem].items():out[mon]=(out.get(mon,0)+c*v)%ns['P']
 out={mon:v for mon,v in out.items() if v}
 assert out==F48[sig],sig
print('Verified all',len(sigs),'sigma: F48(sigma)=sum binom(m,k) k! F47(sigma minus k ones), through degree13')
# Verify propagator identity 1 - X H_even=A and 1-X H_odd=-B.
A,B=ns['A'],ns['B'];P=ns['P']
Heven=[-A[i+1]%P for i in range(13)]
Hodd=[B[i+1] for i in range(13)]
assert [(1 if i==0 else -Heven[i-1])%P for i in range(14)]==A
assert [(1 if i==0 else -Hodd[i-1])%P for i in range(14)]==[(-x)%P for x in B]
print('Verified both tail propagator identities through degree13')
Path('workspace/agent1_tail_check.py').write_text(Path(__file__).read_text())
# Repeat the kappa-zero splitting identity exactly over Q, not just mod p.
from fractions import Fraction
qcode=code.replace('def inv(x):return pow(x,P-2,P)','def inv(x):return Fraction(1,x)').replace('pow(-logA[n],j,P)','((-logA[n])**j)').replace('%P','')
qq={'Fraction':Fraction};exec(qcode,qq)
for n in range(len(qq['BAp']),17):qq['BAp'].append(qq['conv'](qq['BAp'][-1],qq['BA']))
G48={s:qq['f'](s).copy() for s in sigs}
qq['k0']=47;qq['f'].cache_clear();qq['block'].cache_clear()
G47={s:qq['f'](s).copy() for s in sigs}
for sig in sigs:
 m=sig.count(1);out={}
 for k in range(m+1):
  c=math.comb(m,k)*math.factorial(k)
  for mon,v in G47[sig[k:]].items():out[mon]=out.get(mon,0)+c*v
 assert {mon:v for mon,v in out.items() if v}==G48[sig],sig
print('Exact rational kappa-zero splitting verified for all206sigma')
Path('workspace/agent1_tail_check_exact.py').write_text(Path(__file__).read_text())
