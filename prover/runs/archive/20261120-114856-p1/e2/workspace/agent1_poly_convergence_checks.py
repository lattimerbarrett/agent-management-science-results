import sys
sys.path.insert(0,'workspace')
from orthopoly_checks import *
from pathlib import Path
for s in (1,2,3):
 nodes=list(map(S.Integer,range(1,2*s+3)))
 w=[S.Rational(i+1,sum(range(1,len(nodes)+1))) for i in range(len(nodes))]
 w1,p,h=step(nodes,w,s);w2,q,h1=step(nodes,w1,s);w3,r,h2=step(nodes,w2,s)
 ee=p*q-h
 for j in range(s):
  lhs=sum(wi*(r-p).subs(x,t)*t**j for wi,t in zip(w2,nodes))
  rhs=-sum(wi*ee.subs(x,t)**2*p.subs(x,t)*t**j for wi,t in zip(w,nodes))/(h*h1)
  assert S.cancel(lhs-rhs)==0
 print('s',s,'quadratic polynomial increment identity verified rationally')
