import random

def convolution(A,B):
 D=set()
 for a in A:
  for b in B:
   x=a^b
   if x in D:D.remove(x)
   else:D.add(x)
 return D

def qfun(A):
 D=set();L=sorted(A)
 for i,a in enumerate(L):
  for b in L[i+1:]:
   x=a^b
   if x in D:D.remove(x)
   else:D.add(x)
 if (len(A)//2)%2:
  if 0 in D:D.remove(0)
  else:D.add(0)
 return D
rng=random.Random(427)
for n in range(2,6):
 N=1<<n
 for rep in range(100):
  branches=[]
  for _ in range(3):
   A={x for x in range(N) if rng.randrange(2)}
   if len(A)%2:A.symmetric_difference_update({0})
   branches.append(A)
  A,B,H=branches
  F={x+N for x in A}|{x+2*N for x in B}|{x+3*N for x in H}
  qF=qfun(F)
  assert {x-3*N for x in qF if x//N==3}==convolution(A,B)
  assert {x-2*N for x in qF if x//N==2}==convolution(A,H)
  assert {x-N for x in qF if x//N==1}==convolution(B,H)
q={x for x in range(256) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))}
assert len(q)==96
assert convolution(q,{0,1,2,3})==set(range(256))
for v in range(1,256):
 assert {x for x in range(256) if ((x in q)^((x^v) in q))} != set(range(256))
S={0,64,96,112,120,124,126,128,136,144,148,152,154,156}
for w in [322,326,330,334]:
 possible=[(a,b,w-a-b) for a in S for b in S if 0<a<=b<=w-a-b and w-a-b in S]
 # Third branch may exceed156, so only use first/second small branches here.
 for a in [64,96]:
  if a==96:assert (w-a)//2<128
  else:assert all((w-a-b) not in S for b in S if 128<=b<=(w-a)//2)
print('random branch-q convolution identity, all rank4 derivatives, and target arithmetic checked')
