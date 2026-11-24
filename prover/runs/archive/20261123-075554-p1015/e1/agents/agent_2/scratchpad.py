from pathlib import Path
code=r'''"""Exhaustive finite-tree checks of the lower construction's restraint geometry.
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
'''
Path('workspace/agent2_tree_checks.py').write_text(code)
exec(compile(code,'workspace/agent2_tree_checks.py','exec'))
Path('workspace/agent2_restraint_audit.md').write_text(r'''# Restraint-preservation and true-path audit

Write T_sigma for the computable free-domain region of sigma and its descendants,
B_sigma for its own bank, and L_sigma=B_sigma union the finite-child regions.
Put Z_sigma=union L_tau over ancestors tau reached through their infinity child.
A candidate j at sigma installs only finite restraints P disjoint from planned D
and E_sigma,j=Z_sigma union B_sigma union T_(sigma j).

Live-restraint eligibility: if a restraint is owned by tau and tau lies in a
finite child alpha h, then alpha currently has candidate h active. Restraints
in infinity children may persist while that child is paused. Refuting h releases
all restraints in its finite-child region; it never releases infinity-child
restraints.

## Preservation lemma
Consider a destructive action at visited sigma. For a retained restraint owned
by tau:

* If tau is a proper ancestor of sigma, a finite next edge h makes P avoid the
  whole T_(tau h), containing the action. An infinity next edge means tau has
  no active candidate at this visit, so has no own live restraint.
* If tau and sigma are incomparable, take their longest common prefix alpha.
  Distinct finite edges, or sigma's infinity edge against tau's finite edge,
  contradict live-restraint eligibility. The remaining case has sigma in a
  finite child and tau in the infinity child. Then Z_tau includes L_alpha,
  hence contains sigma's entire region.
* If tau extends sigma, during rejection of j its j-child restraints are
  released, other finite children cannot have live restraints, and infinity
  descendants avoid L_sigma via their Z. At an idle/background action sigma
  has no active finite child and only the latter case remains.

Consequently deleting R_sigma,j together with T_(sigma j), or finite background
parts of L_sigma at an infinity visit, misses every retained restraint. Coding
markers are explicitly chosen outside the finite union of live restraints.
All restraints are therefore contained in the final A for as long as they live.

## True path
Visit root and recursively the chosen child down to depth s at stage s. Every
infinitely visited node either has infinitely many infinity visits, or eventually
keeps one candidate j forever. Choose the corresponding child; it is again
infinitely visited. This defines a node at each depth without invoking a
priority-tree theorem.

For every true infinity node sigma, unbounded background initial segments give
L_sigma subset D. Hence Z_sigma subset D for every true-path node sigma.

At a true infinity node of depth e, every actual finite candidate G output by
operator e on x_sigma is eventually selected and refuted (least unrefuted index
fairness). A refutation supplied y in G and a finite (y,H) axiom with no
z in H lying in K_Q, where Q=A_s minus E_sigma,j. In the final set,
A subset Q: planned D_s persists, Z_sigma and B_sigma are eventually in D, and
the j-child region was deleted. Thus H subset C=skip(A), so y is not in skip(C).
No candidate G is contained in skip(C). Meanwhile B_sigma subset D gives
x_sigma in C. Therefore x_sigma witnesses C != Gamma_e(skip(C)).

At a true finite-outcome node, all obligations for its never-refuted G are
processed. Each obtains z and a live finite P subset A with (z,P) in W_z.
Its restraints cannot be released: true finite ancestors never refute their
chosen candidate, and infinity-ancestor refutations release only finite-child
subtrees, not this node. Thus every relevant H meets K_A, giving G subset skip(C).
At activation R_sigma,j still has only finitely many removed points: no
true-path ancestor deletes its whole region, only finite past background cuts
can reach the bank, and j was not previously refuted. Own background stops
forever and descendants cannot touch this bank. An infinite part of R_sigma,j
therefore remains in A. Hence x_sigma not in C but x_sigma in Gamma_e(skip(C)).

The depth-e true node defeats operator e in either case, proving
C not <=_e skip(C). Since cototality is equivalent to X <=_e skip(X), C is not
cototal. The separate coding domain ensures complement(A) has total degree 0'.
''')
