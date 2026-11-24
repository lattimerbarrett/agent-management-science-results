from agent4_relative_sat import instance
from z3 import *
import time

def check():
    # Target forbids {0,1}. Its automorphisms have two orbits of first facets:
    # containing one endpoint, or containing neither.
    for first in (29,60):
        s,fs,t=instance(8,4,stuck=True,seed=False,forbidden=3,timeout=240000)
        s.add(t[fs.index(first)]==1)
        for a in t:s.add(Implies(a>1,Or([b==a-1 for b in t])))
        start=time.time();ans=s.check()
        print('first',first,ans,time.time()-start,flush=True)
        assert ans==unsat
if __name__=='__main__':check()
