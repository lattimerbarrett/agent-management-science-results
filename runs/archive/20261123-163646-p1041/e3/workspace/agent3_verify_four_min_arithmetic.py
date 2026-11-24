import itertools

def verify():
 powers=(0,1,2,4,8,16,32)
 def compatible(a,b):return a==0 or b==0 or a*b<=128
 assert max(a+b for a,b in itertools.product(powers,repeat=2) if a<=16 and b<=16 and compatible(a,b))==24
 assert max(a+b for a,b in itertools.product(powers,repeat=2) if compatible(a,b))==36
 assert max(1+36+24+16,1+24+24+32)<89
 assert 96+1+4+4-2*8==89
 assert 64+1+4+4+16==89
 assert 64+16+1+4+16-2*8==85
 assert 64+0+1+4+16==85
 for u,v in itertools.product((0,1,2,4),repeat=2):
  if 81+u+v>=89:assert u==v==4
 assert 81+4+4-2*2==85
 assert 81+2+8-2*(2+1)==85
 # Q can never improve R beyond P, and costs all W-triples in the core bound.
 for q in (0,1):
  for t in itertools.product(range(q,5),repeat=4):
   T=sum(t)
   assert -2*T+4*q<=0
   if T:assert -2*T+4*q<0
   assert -2*T+4*q<=-2*t[0]
 print('PASS: all four-minword target-exclusion arithmetic')
if __name__=='__main__':verify()
