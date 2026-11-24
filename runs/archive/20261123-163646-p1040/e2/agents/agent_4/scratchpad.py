import sympy as S
from pathlib import Path
z=S.symbols('z');out=[]
for p in [3,5,7,11,13,17,19]:
 f=S.cyclotomic_poly(p,z);b=1+(z-1)**(p-1)
 N=int(S.resultant(f,b,z));r=N%(p*p)
 assert r%p==1 and r!=1
 print('p=c=',p,': norm(1+(zeta_p-1)^(p-1)) mod p² =',r,'nontrivial cyclotomic norm character')
 out.append((p,N,r))
Path('workspace/agent4_odd_hilbert_norm_checks.py').write_text(Path('scratchpad.py').read_text())
