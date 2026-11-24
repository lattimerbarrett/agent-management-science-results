"""Exact self-regenerating certificate excluding indecomposable P4 type(2^2,1^3,0^2).
No published uniform classification is used. See agent3_232_proof.txt.
"""
import sys,time,pickle
from pathlib import Path
sys.path.insert(0,'workspace')
import sympy as S
from agent3_chgeneral import setup
Path('workspace/agent3_232_certificate.py').write_text(Path(__file__).read_text())
t=time.time()
eq,vs=setup((2,3,2))
assert len(vs)==5 and len(eq)==9
G=S.groebner(eq,*reversed(vs),order='grevlex',domain=S.QQ)
a,bb,c,d,e=vs
f=a*(a+d)
quotients,remainder=G.reduce(f)
assert remainder==0
# Independently check the reduction identity in the returned Groebner generators.
assert S.expand(sum(q*g.as_expr() for q,g in zip(quotients,G.polys))-f)==0
L=G.fglm('lex')
assert L.reduce(f)[1]==0
pickle.dump((G,L),open('workspace/agent3_232_certificate_basis.pkl','wb'))
print('QQ Groebner basis has',len(G.polys),'members.')
print('Verified exact ideal membership:',f,'=0.')
print('Hence top q-c1 a=0 or bottom q-c1 -a-d=0 for every complex root.')
print('Elapsed',time.time()-t)
