from z3 import *
import itertools,time,json,numpy as np
s=Solver();s.set(timeout=300000)
d={0:IntVal(15)}
for I in range(1,32):
 d[I]=Int('d%d'%I);s.add(d[I]>=0,d[I]<=15)
for i in range(4):s.add(d[1<<i]==8,d[(1<<i)|16]==7)
s.add(d[16]==14)
for A in range(32):
 for B in range(32):
  if A&B==A:s.add(d[A]>=d[B])
  s.add(d[A]+d[B]<=d[A|B]+d[A&B])
for J in range(1,16):s.add(d[J]-d[J|16]>=0,d[J]-d[J|16]<=1)
for labs in itertools.product(range(5),repeat=5):
 A=B=C=D=0
 for i,z in enumerate(labs):
  if z==1:A|=1<<i
  elif z==2:B|=1<<i
  elif z==3:C|=1<<i
  elif z==4:D|=1<<i
 if not A or not B or not C or not D:continue
 def r(J):return 15-d[J]
 s.add(r(A|B)+r(A|C)+r(A|D)+r(B|C)+r(B|D)>=r(A)+r(B)+r(C|D)+r(A|B|C)+r(A|B|D))
def term(J):return If(d[J]>d[J|16],Sum([If(d[J]==i,2**(i-1),0) for i in range(1,9)]),0)
w=512-2*Sum([term(j) for j in range(1,16) if j.bit_count()==2])+4*Sum([term(j) for j in range(1,16) if j.bit_count()==3])-8*term(15)
# To enumerate further profiles at a target, fix w then exclude each already ruled-out profile.
# IMPORTANT: satisfiability is only a NECESSARY rank-profile condition, not subspace realization.
for target in [322,326,330,334]:
 s.push();s.add(w==target);t=time.time()
 r=s.check();print(target,r,time.time()-t,flush=True)
 if r==sat:print({i:s.model().eval(d[i]).as_long() for i in d},flush=True)
 s.pop()
