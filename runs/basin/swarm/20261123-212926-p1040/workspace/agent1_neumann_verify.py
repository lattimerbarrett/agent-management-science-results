"""Exact verification/export of Neumann's 11 Aut(F3) relators.
Input finite presentation copied from FGA AutGrp.gi; all identities checked
by reduced free words independently, before any source inference.
"""
import json
from itertools import permutations

def inv(w):return tuple(-i for i in w[::-1])
def cat(*ws):
 z=[]
 for w in ws:
  for i in w:
   if z and z[-1]==-i:z.pop()
   else:z.append(i)
 return tuple(z)
def subst(w,A):return cat(*(A[i-1] if i>0 else inv(A[-i-1]) for i in w))
def compose(A,B):return tuple(subst(w,A) for w in B)
def power(w,n):
 if n<0:w=inv(w);n=-n
 return cat(*(w for _ in range(n)))
def cm(a,b):return cat(inv(a),inv(b),a,b) # GAP commutator
I=((1,),(2,),(3,))
S,T,U=(1,),(2,),(3,)
s=lambda n:power(S,n)
t=lambda n:power(T,n)
u=lambda n:power(U,n)
rels=[power(cat(s(5),t(-1)),2),
 cat(t(-1),S,t(2),s(8),t(-1),S,t(2),s(-4)),
 power(cat(s(4),t(-1),S,t(-1)),2),t(4),
 cm(U,cat(s(2),t(-1),S,t(-1),s(2))),
 cm(U,cat(s(-2),t(-1),S,t(-1),U,s(-2),t(-1),S,t(-1))),
 cm(U,cat(s(-2),t(-1),S,T,S,t(-1),U,T,s(-1),t(-1),s(-1),T,s(2))),
 cm(U,cat(t(-1),S,t(2),U,t(-1),S,t(2))),
 cat(s(-2),t(-1),S,t(2),s(2),U,s(2),t(-1),S,t(2),s(2),U,s(-2),U,s(2),u(-1),s(-2),u(-1)),
 power(cat(s(-2),t(-1),S,T,U),2),power(cat(U,T),3)]
STU=[((-2,),(-3,),(-1,)),((2,),(-1,),(3,)),((1,2),(2,),(3,))]
# inverses for signed STU evaluation
STUi=[power((1,),1)]*3
STUi=[(( -3,),(-1,),(-2,)), ((-2,),(1,),(3,)),((1,-2),(2,),(3,))]
for a,b in zip(STU,STUi):assert compose(a,b)==compose(b,a)==I
for r in rels:
 A=I
 for x in r:A=compose((STU if x>0 else STUi)[abs(x)-1],A)
 assert A==I,(r,A)
# Same 10 Nielsen automorphisms as agent4 data, acted successively on left.
ags=[((-1,),(2,),(3,))]
ags += [tuple((i,) for i in p) for p in permutations((1,2,3)) if p!=(1,2,3)]
ags += [((2,1),(2,),(3,)),((-2,1),(2,),(3,)),((1,-2),(2,),(3,)),((1,2),(2,),(3,))]
ai={i:next(j for j,b in enumerate(ags) if compose(a,b)==compose(b,a)==I) for i,a in enumerate(ags)}
seen={I:()};front=[I]
for radius in range(1,8):
 if all(a in seen for a in STU):break
 nxt=[]
 for old in front:
  for j,g in enumerate(ags):
   A=compose(g,old)
   if A not in seen:seen[A]=seen[old]+(j,);nxt.append(A)
 front=nxt
assert all(a in seen for a in STU)
words=[seen[a] for a in STU]
expanded=[]
for r in rels:
 w=tuple(j for x in r for j in (words[x-1] if x>0 else tuple(ai[j] for j in words[-x-1][::-1])))
 A=I
 for j in w:A=compose(ags[j],A)
 assert A==I
 expanded.append(w)
if __name__=='__main__':
 print('STU Nielsen words',words)
 print('11 verified relator lengths STU',list(map(len,rels)))
 print('11 verified relator lengths Nielsen',list(map(len,expanded)))
 data={'STU_images':STU,'STU_words_in_10endos':words,'STU_relators':rels,'nielsen_relators':expanded,'convention':'0based10endoindices; append composes new automorphism on left'}
 from pathlib import Path
 Path('workspace/agent1_neumann_relators.json').write_text(json.dumps(data))
