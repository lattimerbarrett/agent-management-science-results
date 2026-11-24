from pathlib import Path
import runpy,numpy as np
m=runpy.run_path('experiments/e1/agent1_compact_D7_conflict_certificate.py')
comm,inv=m['comm'],m['inv']
def T(a,b,c,g):return comm(comm(comm((a,),(b,)),(c,)),(-g,))
W=T(1,9,4,2)+T(1,9,4,5)+T(5,4,9,1)+inv(T(5,8,9,4))
S,E,words=m['scalar'](7,0)
V=E.copy();bound=0
for a in reversed(W):
 V=S[a]@V;bound=max(bound,int(np.max(np.abs(V))))
V-=E
print('maximum intermediate coefficient:',bound)
for d in range(1,8):
 rows=[i for i,w in enumerate(words) if len(w)==d]
 v=V[rows]
 print('Magnus wordlength',d,': nonzero displacement coefficients',np.count_nonzero(v))
 if d==6:
  nz=np.argwhere(v)
  for r,j in nz[:5]: print(' output',j,'word',words[rows[r]],'coefficient',int(v[r,j]))
print('Index rule: wordlength d first appears iff automorphism lies in A_(d-2) but not A_(d-1), for d>=2? CHECK BELOW')
print('Correct rule: first displacement length d means A_(d-1) minus A_d.')
p=Path('experiments/e1/agent4_degree6_primitive_cokernel.json')
print('\nDegree-six image metadata:',p.read_text()[:8000])