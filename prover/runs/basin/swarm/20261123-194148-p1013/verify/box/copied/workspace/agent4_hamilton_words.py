from functools import lru_cache

def words(parts,cycle):
 r=len(parts);ans=0
 for first in range(r):
  if not parts[first]:continue
  @lru_cache(None)
  def f(left,last):
   if not any(left):return int(not cycle or last!=first)
   out=0
   for j in range(r):
    if left[j] and j!=last:
     a=list(left);a[j]-=1;out+=f(tuple(a),j)
   return out
  left=list(parts);left[first]-=1
  ans+=f(tuple(left),first)
 return ans
for r in [3,4]:
 for m in [3,6,12,18]:
  full=(m,)*r;core=(m-1,)+(m,)*(r-1)
  ratio=r*words(core,False)/words(full,True)
  print(r,m,ratio,'target',r*r/(r-1)**2)
open('workspace/agent4_hamilton_words.py','w').write(open(__file__).read())
