import runpy,numpy as np
m=runpy.run_path('experiments/e1/agent1_compact_D7_conflict_certificate.py')
# Replace commutator transvections by LEFT multiplication as in the new witnesses.
oldgens=m['gens']
def leftgens():
 G=oldgens()
 for a in (3,6,9):
  for signed in (a,-a):
   imgs=G[signed]
   for i,w in enumerate(imgs):
    if len(w)>1:
     imgs[i]=w[1:]+w[:1]
 return G
m['scalar'].__globals__['gens']=leftgens
S,E,words=m['scalar'](4,0)
# D=K12 (1), A=C1;23 (3), B=C3;12 (9).
w=m['comm']((1,),m['comm']((3,),(9,)))
V=m['evaluate'](w,S,E,0)
print('Uniform cubic witness [K12,[C1;23,C3;12]]:')
print('integral action through degree4 is identity:',not V.any())
import sympy as sp
x=sp.symbols('x')
f=x*x+3*x+3
print('Q3(zeta3), pi=zeta3-1, minimal polynomial:',f)
print('Norm(1+pi^2) =',sp.resultant(f,1+x*x,x),'(not 1 mod 9)')
print('This is the critical cubic Hilbert-symbol detector.')