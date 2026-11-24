import sys,itertools
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_tensor import *

def W(t):
 out=(t[0]+1,)
 for q in t[1:]:out=commutator_word(out,(q+1,))
 return out
terms=[((0,5,2),3),((0,2,5),-1),((0,1,1),-4),((1,2,3),-2)]
u=()
for t,a in terms:
 w=W(t)
 if a<0:w=inverse_word(w)
 u+=w*abs(a)
reflectionimages=[(1,),(0,),(0,1),(2,),(0,),(0,2),(2,),(1,),(1,2)]
rword=[]
for q in u:
 im=reflectionimages[abs(q)-1]
 if q<0:im=im[::-1]
 for r in im:
  if rword and rword[-1]==r:rword.pop()
  else:rword.append(r)
P={()}
for r in rword:
 Q=P.copy()
 for w in P:
  if len(w)<3 and (not w or w[-1]!=r):
   v=w+(r,)
   if v in Q:Q.remove(v)
   else:Q.add(v)
 P=Q
print('sourcewordlength',len(u),'reflectionwordlength',len(rword))
print('target Magnus throughdegree3:',sorted(''.join('ABC'[x] for x in w) for w in P))
assert all(len(w)==3 or not w for w in P) and len(P)>1
