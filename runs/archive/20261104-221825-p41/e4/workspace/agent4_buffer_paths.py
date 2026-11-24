import json,itertools
from pathlib import Path
from collections import Counter

def buffer_leaves(c,U,M=(),P=0):
 if c[0]=='simplex':
  rank=c[1].bit_count()
  M=set(M);loops=0
  for m in M:
   if m.bit_count()==1:loops|=m
  active=U&~loops
  M={m for m in M if not m&loops and m.bit_count()<=rank}
  M={m for m in M if not any(z!=m and z&m==z for z in M)}
  used=0
  for m in M:used|=m
  p=(active&~used).bit_count()
  return [(rank,p,tuple(sorted(M)),c[1],U)]
 _,s,D,L=c
 return buffer_leaves(D,U,M+(s,),P)+buffer_leaves(L,U&~s,tuple(m&~s for m in M),P|s)
