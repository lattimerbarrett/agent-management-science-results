from agent4_cone_sat import instance
from z3 import *
import time

def check():
    # First two shelling facets share a ridge. After relabeling they are
    # 15={0,1,2,3},23={0,1,2,4}. A distinguished vertex has three orbits.
    for vbit in (1,8,32):
        s,fs,t=instance(8,4,stuck=True,seed=True,vbit=vbit,timeout=240000)
        s.add(t[1]==2)
        for a in t:s.add(Implies(a>1,Or([b==a-1 for b in t])))
        start=time.time();ans=s.check()
        print('vbit',vbit,ans,time.time()-start,flush=True)
        assert ans==unsat
if __name__=='__main__':check()
