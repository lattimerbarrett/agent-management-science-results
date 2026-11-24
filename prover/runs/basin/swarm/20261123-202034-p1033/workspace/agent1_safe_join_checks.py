from pathlib import Path
from itertools import combinations
import json,math,time
n=8;m=2;t=n*m;r=n-2*m;d=r+m*(2*m-1)
edges=list(combinations(range(n),2));idx={e:j for j,e in enumerate(edges)}
star=[sum(1<<idx[tuple(sorted((a,b)))] for b in range(n) if b!=a) for a in range(n)]
old=[];closed=[]
for a in range(n):
 es=[j for j in range(len(edges)) if star[a]>>j&1]
 for h in range(m):
  owner=a*m+h
  for s in range(r,len(es)+1):
   for comb in combinations(es,s):
    P=sum(1<<j for j in comb)
    omit=[b for b in range(n) if b!=a and not(P>>idx[tuple(sorted((a,b)))]&1)]
    T=sum(1<<(b*m+j) for b in omit for j in range(m))
    assert P.bit_count()+T.bit_count()<=d
    row=(owner,P,T);closed.append(row)
    if s==r:old.append(row)
# Every classwise join of two oldpatterns is in the saturated class family.
closedset=set(closed);joins=0
for a,b in combinations(old,2):
 if a[0]!=b[0]:continue
 j=(a[0],a[1]|b[1],a[2]&b[2]);assert j in closedset;joins+=1
checks=0
for i,(owner,P,T) in enumerate(closed):
 for owner2,Q,U in closed[:i]:
  if owner==owner2:continue
  assert (P&Q) or (T>>owner2&1) or (U>>owner&1)
  checks+=1
# All target-free full-star seedpatterns occur.
assert all((a*m+h,star[a],0) in closedset for a in range(n) for h in range(m))
row=dict(n=n,m=m,t=t,old_patterns=len(old),join_closed_patterns=len(closed),classwise_old_pairs=joins,cross_closed_pairs_verified=checks,max_residual=d,seed_residual=n-1)
print(json.dumps(row,indent=2))
Path('workspace/agent1_safe_join_checks.json').write_text(json.dumps(row,indent=2))
Path('workspace/agent1_safe_join_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_safe_join_lemma.txt').write_text('''SAFE JOIN CLOSURE IN THE SEPARATED ALL-CHOICE MODEL
A pattern of owneri is (P,T), with actualsetP outsideallcores and targetlabelsT notcontainingi.
For a finite nonemptycollectionofsame-ownerpatterns define itsJOIN as
(union P, intersection T). Joins from ANY owners remain mutuallycompatible.
Indeed if unionP_i and unionQ_j aredisjoint andownerk isNOTin intersectionT_i,
chooseonei withk notinT_i. CompatibilitywithEVERYoldQ_j thenforcesownerh inEVERYU_j,
henceownerh in intersectionU_j. This proves crosspatterncondition.
Thus addingALLjoins ofatmostLoldpatterns/class preservesintersection simultaneously,
notmerelyoneatatime. ResidualcapincreasesatmostfactorL (actualunions and targetintersection).
Ifm=t classes andtau=t, canonicalcoretransversalkeepscovertau=t afteradditions.
Moregenerallyifthereisanactualrank-tauseedmemberbeforejoining, thatoldmembercoversALLjoins,
soaddingjoinsalsopreservestauinthearbitrary-mtau-onlymodel.

HEAVY-MENU DICHOTOMY. StartwithonetargetsetM (size<=d).
While|M|>sqrt(d) andsomeoldtargetsetT has|M intersect T|<=|M|/2,
jointhatpattern; Mhalves. Afteratmost1+ceil(log2d)selectedpatterns,either
|M|<=sqrt(d), oreveryoldpatterncontainsMORETHAN|M|/2targetsinM.
The joinedactualsethasatmostr(1+ceil(log2d))points.
This is an exact dichotomy, NOT yet an asymptoticbound: replacingoldpatternsbyjoinscanLOWERtau,
andnooneglobalexceptionsetcapturingtheper-classheavyMhasbeenfound.

ACTUALCHECK: duplicatecenterconstructionm2,n8,t16,d10 has560oldpatterns.
Classwisejoinclosureis1024patterns(allactualstarsubsetssize>=4), stillcap10.
Allclasswiseoldpairs andALLcrossclosedpairs checkedexplicitly; all16targetfreefull-star
rank16seedsappear. This verifiesnontrivialjoinswithDECREASINGresidualcost.
''')
