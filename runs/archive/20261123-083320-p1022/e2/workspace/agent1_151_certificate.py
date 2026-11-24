"""Exact P4 consecutive multiplicity (1,5,1) certificate."""
import sys
sys.path.insert(0,'workspace')
from agent1_incidence import system,S
vs,es,_=system((1,5,1))
g=S.groebner(es,*vs)
a,b=vs[0],vs[-1]
assert g.reduce((a*b)**3)[1]==0
# Therefore every complex Chern solution has one extremal Grassmannian
# line factor trivial; that extremal HN piece descends to P4.
print('P4 (1,5,1): exact ideal membership (a*b)^3=0 certified.')
