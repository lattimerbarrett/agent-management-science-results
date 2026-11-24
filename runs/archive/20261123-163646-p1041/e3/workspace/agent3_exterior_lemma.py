"""Checks the exterior-form lemma used in the conditional126-slice argument.
GL(U)xGL(V) orbits of6-spaces W⊂U⊕V are determined by
(a,b,c)=(dim(W∩U),dim(W∩V),6-a-b).
"""
from itertools import combinations

def wedge(form,vector):
 out=set()
 for mask in form:
  for i in range(12):
   if vector>>i&1 and not(mask>>i&1):
    j=mask|1<<i
    if j in out:out.remove(j)
    else:out.add(j)
 return out

def rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)

def essential_dimension(form):
 indices={sum(1<<i for i in group):j for j,group in enumerate(combinations(range(12),5))}
 rows=[]
 for i in range(12):
  row=0
  for mask in form:
   if mask>>i&1:row^=1<<indices[mask^(1<<i)]
  rows.append(row)
 return rank(rows)

def divisor_dimension(form):
 indices={sum(1<<i for i in group):j for j,group in enumerate(combinations(range(12),7))}
 rows=[]
 for i in range(12):
  row=0
  for mask in wedge(form,1<<i):row^=1<<indices[mask]
  rows.append(row)
 return 12-rank(rows)

def verify():
 alpha={0x3f,0xfc0}
 got=set()
 count=0
 for a in range(7):
  for b in range(7-a):
   c=6-a-b
   vectors=[1<<i for i in range(a)]+[1<<(6+i) for i in range(b)]
   vectors +=[(1<<(a+i))^(1<<(6+b+i)) for i in range(c)]
   beta={0}
   for v in vectors:beta=wedge(beta,v)
   assert len(vectors)==6
   gamma=alpha.symmetric_difference(beta)
   d=essential_dimension(gamma)
   got.add(d);count+=1
   assert d in {6,11,12},(a,b,c,d)
   if d==11:
    assert (a,b,c) in {(5,0,1),(0,5,1)}
    assert divisor_dimension(gamma)==1
 assert got=={6,11,12}
 print('Every essential-dimension11 form also has common-linear-divisor dimension1.')
 print('Checked all',count,'GL(6,2)xGL(6,2) orbit types: essential dimensions',sorted(got))
if __name__=='__main__':verify()
