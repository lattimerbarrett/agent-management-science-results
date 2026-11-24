from agent4_export_gap_seeds import mul,inv,comm
from itertools import permutations
def invword(w):return tuple(-i for i in w[::-1])
def reduceword(w):
 o=[]
 for i in w:
  if o and o[-1]==-i:o.pop()
  else:o.append(i)
 return tuple(o)
def substitute(w,a):return reduceword(j for i in w for j in (a[i-1] if i>0 else invword(a[-i-1])))
def compose(a,b):return tuple(substitute(w,a) for w in b)
identity=((1,),(2,),(3,))
ags=[((-1,),(2,),(3,))]+[tuple((i,) for i in p) for p in permutations((1,2,3)) if p!=(1,2,3)]+[((2,1),(2,),(3,)),((-2,1),(2,),(3,)),((1,-2),(2,),(3,)),((1,2),(2,),(3,))]
from pathlib import Path
import json

def power(w,n):return mul(*((w if n>=0 else inv(w)),)*abs(n))
S=(1,);T=(2,);U=(3,)
def sp(n):return power(S,n)
def tp(n):return power(T,n)
def up(n):return power(U,n)
rels=[power(mul(sp(5),tp(-1)),2),mul(tp(-1),S,tp(2),sp(8),tp(-1),S,tp(2),sp(-4)),power(mul(sp(4),tp(-1),S,tp(-1)),2),tp(4),comm(U,mul(sp(2),tp(-1),S,tp(-1),sp(2))),comm(U,mul(sp(-2),tp(-1),S,tp(-1),U,sp(-2),tp(-1),S,tp(-1))),comm(U,mul(sp(-2),tp(-1),S,T,S,tp(-1),U,T,sp(-1),tp(-1),sp(-1),T,sp(2))),comm(U,mul(tp(-1),S,tp(2),U,tp(-1),S,tp(2))),mul(sp(-2),tp(-1),S,tp(2),sp(2),U,sp(2),tp(-1),S,tp(2),sp(2),U,sp(-2),U,sp(2),up(-1),sp(-2),up(-1)),power(mul(sp(-2),tp(-1),S,T,U),2),power(mul(U,T),3)]
# Find lifts of S,T and inverses using finite signed-permutation group.
seen={identity:()};front=[identity]
while front:
 nxt=[]
 for A in front:
  for j,g in enumerate(ags[:6]):
   B=compose(g,A)
   if B not in seen:seen[B]=seen[A]+(j,);nxt.append(B)
 front=nxt
STU=[((-2,),(-3,),(-1,)),((2,),(-1,),(3,)),((1,2),(2,),(3,))]
STUi=[((-3,),(-1,),(-2,)),((-2,),(1,),(3,)),((1,-2),(2,),(3,))]
conv={1:seen[STU[0]],-1:seen[STUi[0]],2:seen[STU[1]],-2:seen[STUi[1]],3:(9,),-3:(8,)}
assert len(seen)==48
out=[]
for i,r in enumerate(rels):
 A=identity
 for x in r:A=compose((STU if x>0 else STUi)[abs(x)-1],A)
 assert A==identity,(i,r,A)
 w=sum((conv[x] for x in r),())
 A=identity
 for j in w:A=compose(ags[j],A)
 assert A==identity,(i,w,A)
 out.append({'name':'19'+chr(97+i),'STU_word':r,'Nielsen_word':w})
if __name__=='__main__':
 Path(__file__).with_suffix('.json').write_text(json.dumps({'citation':'B. H. Neumann presentation via GAP FGA AutGrp.gi, n=3, eq19a-k','convention':'words append new automorphism on left, same as GAP LTR; Nielsen0based same as agent4_gap_ia3_data.json','STU_Nielsen_lifts':conv,'rels':out},indent=2))
 print('All11 NeumannAutF3relators verified exactly, Nielsengths',[len(r['Nielsen_word']) for r in out])
