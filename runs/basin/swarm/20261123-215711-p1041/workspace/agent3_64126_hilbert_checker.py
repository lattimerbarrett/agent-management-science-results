from itertools import combinations

def wedge(A,B):
 C=set()
 for a in A:
  for b in B:
   if not a&b:
    c=a|b
    if c in C:C.remove(c)
    else:C.add(c)
 return C

def rank(rows):
 piv={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in piv:r^=piv[p]
   else:piv[p]=r;break
 return len(piv)

def masks(k):
 return [sum(1<<j for j in S) for S in combinations(range(12),k)]

def flatten(T,k):
 cols=masks(6-k)
 return rank([sum(1<<j for j,J in enumerate(cols) if not I&J and (I|J) in T) for I in masks(k)])

expected=[(30,40),(38,52),(42,58),(44,60),(45,60)]
for d in range(1,6):
 G={0}
 for i in range(6):G=wedge(G,{1<<(6+i),1<<i} if i<d else {1<<(6+i)})
 omega={63,4032}^G
 T={4095^I for I in omega}
 R2,R3=flatten(T,2),flatten(T,3)
 assert (R2,R3)==expected[d-1]
 if d>=2:assert 26+2*R2+R3>144
 print(d,R2,R3,26+2*R2+R3)
print('All graph-top moment flattenings checked exactly')
