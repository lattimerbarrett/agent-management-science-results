from fractions import Fraction as F
from agent1_cycle_counter import internal_component_cycles,star,path

def gap(r,k):
 return -1+2*F(k-1,k*(r-1))+F((r-2)*(k-2)*(k-3),2*k*(r-1)**2)

def exact_r4(q):
 u=8*q
 a=internal_component_cycles([u+3,u+3,u+2,u+2],[star(7)]*(q-1)+[star(10)])
 b=internal_component_cycles([u+4,u+2,u+2,u+2],[path(7)]*q+[path(3)])
 return F(b,a)-1

if __name__=='__main__':
 import sympy as s
 r,k=s.symbols('r k')
 g=-1+2*(k-1)/(k*(r-1))+(r-2)*(k-2)*(k-3)/(2*k*(r-1)**2)
 assert s.simplify(g.subs(k,2*r+1)-3/((r-1)*(2*r+1)))==0
 assert s.simplify(g.subs(k,2*r)+(r-4)/(2*r*(r-1)))==0
 assert gap(3,6)==F(1,12)
 assert gap(4,8)==0
 for q in range(1,7):
  z=exact_r4(q)
  assert z>0
  print('r4 q',q,'exact ratio >1; relative gain',float(z),'scaled',float(z*(32*q+10)**2))
 for r,k,maxq in [(3,6,5),(5,11,3),(6,13,2)]:
  for q in range(1,maxq+1):
   u=k*q
   a=internal_component_cycles([u+3,u+3]+[u+2]*(r-2),[star(k-1)]*(q-1)+[star(k+2)])
   b=internal_component_cycles([u+4]+[u+2]*(r-1),[path(k-1)]*q+[path(3)])
   assert b>a
   print('r,k,q',r,k,q,'exact path beats star')
 print('All exact checks passed')
