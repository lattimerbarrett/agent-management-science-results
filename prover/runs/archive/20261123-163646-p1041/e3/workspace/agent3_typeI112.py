"""Apolar calculation for a decomposable6-form plus KT type-I112 form.
If their wedge pairing is nonzero in dimension12, GL-reduction is unique:
write gamma=D2 wedge rho4 on M=D2+Q6, rho4 dual to nondegenerate2-form onQ6.
The6-space W of beta must intersectM in E2 with E wedge gamma!=0.
Shears from complement N4 intoM make W=E+N4. E is transverseD and projects
to a nondegenerate symplectic2-plane inQ6, hence is conjugate to <q1,q2>.
"""
from itertools import combinations

def rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)

def verify():
 terms=[(0,1,2,3,4,5),(0,1,2,3,6,7),(0,1,4,5,6,7),(2,3,8,9,10,11)]
 form={sum(1<<i for i in I) for I in terms}
 ranks=[]
 for k in range(7):
  rows=[]
  for I in combinations(range(12),k):
   mask=sum(1<<i for i in I);row=0
   for a in form:
    if a&mask==mask:row^=1<<(a^mask)
   rows.append(row)
  ranks.append(rank(rows))
 assert ranks==[1,12,42,60,42,12,1]
 assert sum(ranks)==170>158
 print('Type-I112 plus decomposable, nonzero wedge pairing: ranks',ranks,'length170.')
if __name__=='__main__':verify()
