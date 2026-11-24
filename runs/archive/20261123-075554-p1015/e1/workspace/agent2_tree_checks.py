"""Exhaustive finite-tree checks of the lower construction's restraint geometry.
None is a check of the infinite true-path or limit-existence argument.
"""
from itertools import product
INF=-1

def prefix(a,b): return b[:len(a)]==a

def run_checks(depth=4, outcomes=(INF,0,1)):
    nodes=[s for d in range(depth+1) for s in product(outcomes,repeat=d)]
    U=set(nodes) # one representative point per node bank suffices for regions
    def region(s): return {t for t in U if prefix(s,t)}
    def body(s):
        return {s}|set().union(*(region(s+(j,)) for j in outcomes if j!=INF))
    def Z(s):
        return set().union(*(body(s[:i]) for i,x in enumerate(s) if x==INF)) if INF in s else set()
    def exclusion(s,j): return Z(s)|{s}|region(s+(j,))
    def merge(constraints, key,value):
        if key in constraints and constraints[key]!=value: return False
        constraints[key]=value; return True
    def visit_constraints(s):
        # A node is visited by taking the currently chosen edge at each ancestor.
        return {s[:i]:(None if x==INF else x) for i,x in enumerate(s)}
    count_bg=count_fail=0
    for s in nodes:
      if len(s)>=depth: continue
      for failure in (False,True):
       for j in ([0,1] if failure else [None]):
        current=visit_constraints(s)
        current[s]=j
        deleted=({s}|region(s+(j,))) if failure else body(s)
        # Whole bank s is overestimated in failure: actual action removes only R_j.
        for t in nodes:
         if t==s or (failure and prefix(s+(j,),t)): continue # released restraints
         for k in [0,1]:
          constraints=dict(current)
          possible=merge(constraints,t,k)
          # A retained restraint in a finite child exists only while that outcome
          # remains active. Infinite-child restraints may remain while paused.
          for i,x in enumerate(t):
           if x!=INF: possible=possible and merge(constraints,t[:i],x)
          if not possible: continue
          assert deleted <= exclusion(t,k),(s,j,t,k,deleted-exclusion(t,k))
          if failure: count_fail+=1
          else: count_bg+=1
    # Final destined-zero geometry: Z(node) includes each infinite ancestor body.
    for t in nodes:
      for i,x in enumerate(t):
       if x==INF: assert body(t[:i])<=Z(t)
    return {'nodes':len(nodes),'background_restraint_pairs':count_bg,
            'failure_restraint_pairs':count_fail,'depth':depth}

if __name__=='__main__': print(run_checks())
