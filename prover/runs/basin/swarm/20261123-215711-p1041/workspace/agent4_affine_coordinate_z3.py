from z3 import *
import time
s=Solver()
D={}
for I in range(16):
 C=15^I;first=C&-C
 for P in range(16):
  if P&~C or P&first:continue
  v=Int('d%d_%d'%(I,P));D[I,P]=v;s.add(v>=0,v<=14)
for j in range(4):s.add(Sum([v for (I,P),v in D.items() if I>>j&1])==7)
s.add(Sum(list(D.values()))<=14)
def inter(J):return Sum([v for (I,P),v in D.items() if I&J==J])
def nonempty(J):return And([v==0 for (I,P),v in D.items() if (J&~I&P) and (J&~I&~P)])
def power(x):return Sum([If(x==i,2**i,0) for i in range(8)])
def term(J):return If(nonempty(J),power(inter(J)),0)
w=512-2*Sum([term(j) for j in range(1,16) if j.bit_count()==2])+4*Sum([term(j) for j in range(1,16) if j.bit_count()==3])-8*term(15)
for target in [322,326,330,334]:
 s.push();s.add(w==target);r=s.check();print(target,r,flush=True);assert r==unsat;s.pop()
