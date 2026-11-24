"""Literal transcription of n=3 seed construction in GAP LPRES examples.gi.
Tuples encode words in GAP's generator ordering; GAP operation conventions retained.
"""
from itertools import permutations,product
from collections import Counter
import json
from pathlib import Path

def red(w):
 o=[]
 for x in w:
  if o and o[-1]==-x:o.pop()
  else:o.append(x)
 return tuple(o)
def mul(*ws):return red(sum(ws,()))
def inv(w):return tuple(-x for x in w[::-1])
def div(a,b):return mul(a,inv(b))
def conj(a,b):return mul(inv(b),a,b)
def comm(a,b):return mul(inv(a),inv(b),a,b)

def run(n=3):
 C={};M={};names=[]
 for i,j in permutations(range(1,n+1),2):
  names.append(('C',i,j));C[i,j]=(len(names),);C[i,j+n]=(-len(names),)
 for a,b,c in permutations(range(1,n+1),3):
  if b>c:continue
  names.append(('M',a,b,c));M[a,b,c]=(len(names),);M[a,c,b]=(-len(names),)
  M[a,c,b+n]=conj(M[a,b,c],C[a,b])
  M[a,b,c+n]=conj(M[a,c,b],C[a,c])
  M[a,c+n,b+n]=conj(M[a,b,c+n],C[a,b])
  M[a,b+n,c+n]=conj(M[a,c,b+n],C[a,c])
  M[a,c+n,b]=conj(M[a,b,c],C[a,c])
  M[a,b+n,c]=conj(M[a,c,b],C[a,b])
  for s,t in product([0,n],repeat=2):
   M[a+n,b+s,c+t]=div(comm(inv(C[a,b+s]),inv(C[a,c+t])),M[a,b+s,c+t])
   M[a+n,c+s,b+t]=div(comm(inv(C[a,c+s]),inv(C[a,b+t])),M[a,c+s,b+t])
 rel=[]
 def put(f,w):rel.append((f,red(w)))
 for a,b,c in permutations(range(1,n+1),3):
  for s,t,u in product([0,n],repeat=3):put('R0',mul(M[a+s,b+t,c+u],M[a+s,c+u,b+t]))
 for a,b in permutations(range(1,n+1),2):
  if (a,b)!=(1,2):continue
  for c,d in permutations(range(1,n+1),2):
   if a!=c and a!=d and b!=c:put('R1',comm(C[a,b],C[c,d]))
 for a,b,c in permutations(range(1,n+1),3):
  if (a,b)!=(1,2):continue
  for s,t,u in product([0,n],repeat=3):
   for d,e,f in permutations(range(1,n+1),3):
    if e>f:continue
    for v,w,x in product([0,n],repeat=3):
     if a+s!=d+v and a not in (e,f) and d not in (b,c):put('R2',comm(M[a+s,b+t,c+u],M[d+v,e+w,f+x]))
 # R3 requires four distinct labels; absent at n3.
 for a,b,c in permutations(range(1,n+1),3):
  if (a,b)!=(1,2):continue
  put('R4',comm(mul(C[c,b],C[a,b]),C[c,a]))
  for s,t,u in product([0,n],repeat=3):
   put('R5',div(conj(M[a+s,b+t,c+u],C[a,b+t]),M[a+s,c+u,b+n-t]))
   put('R6',div(mul(M[a+n-s,b+t,c+u],M[a+s,b+t,c+u]),comm(inv(C[a,b+t]),inv(C[a,c+u]))))
 # R7,R8 require four distinct labels; absent at n3.
 for a,b,c in permutations(range(1,n+1),3):
  if (a,b)!=(1,2):continue
  for d in range(1,n+1):
   if d in (a,c):continue
   for s,t,u,v in product([0,n],repeat=4):
    put('R9',div(mul(M[c+u,b+t,a+s],M[c+u,a+s,d+v],conj(M[c+u,a+s,b+t],C[c,d+n-v])),conj(M[c+u,a+s,d+v],C[a,b+t])))
 out={'convention':'GAP left-to-right map products, comm=x^-1 y^-1 x y','names':names,'rels':[{'family':f,'word':w} for f,w in rel]}
 print('all',Counter(f for f,w in rel),'nonempty',Counter(f for f,w in rel if w),'unique nonempty',len(set(w for f,w in rel if w)))
 return out,C,M
if __name__=='__main__':
 out,_,_=run();Path(__file__).with_name('agent4_gap_ia3_seeds.json').write_text(json.dumps(out,indent=2))
