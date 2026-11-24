import sys,itertools,random
sys.path.insert(0,'experiments/e1')
from q_dimension_checks import maximal_intersecting,check_suitable
for k in [3,4,5]:
 Fs=maximal_intersecting(k); U=(1<<k)-1
 pairs=[(a,U^a) for a in range(1<<k) if a<(U^a)]
 for typ in ['sizeup','sizedown','mask','common']:
  orders=[]
  for i in range(k):
   p=pairs[:]
   if typ!='common':
    p.sort(key=lambda ab: ((1 if typ=='sizeup' else -1)*(ab[0] if ab[0]>>i&1 else ab[1]).bit_count() if typ in ['sizeup','sizedown'] else 0,ab[0] if ab[0]>>i&1 else ab[1]))
   def key(F):return tuple(int(bool((a if a in F else b)&(1<<i))) for a,b in p)
   orders.append(sorted(range(len(Fs)),key=lambda j:key(Fs[j])))
  print(k,typ,check_suitable(orders,len(Fs)))
