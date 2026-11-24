import sys,itertools as it,json,time
from fractions import Fraction
sys.path.insert(0,'workspace');from agent1_cycle_counter import *
results=[]
for m in [20,40,80,160,320]:
 n=2*m+1;start=time.time();C=multipartite_component_cycles([m+1,m],[[star(4)],[]]);out=[]
 for typA,typB in it.product(['S','T'],repeat=2):
  A=star(3) if typA=='S' else triangle();B=star(3) if typB=='S' else triangle()
  E=multipartite_component_cycles([m+1,m],[[A],[B]])
  out.append({'types':typA+typB,'sign':(C>E)-(C<E),'scaled':float(Fraction(n*(C-E),E))})
 r={'n':n,'comparisons':out,'seconds':time.time()-start};results.append(r);print(r,flush=True)
 with open('workspace/agent3_r2_cycles.json','w') as f:json.dump(results,f)
