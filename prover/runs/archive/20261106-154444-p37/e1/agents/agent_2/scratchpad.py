import random,itertools
random.seed(128)
# Independent direct grouped-lex audit on arbitrary intersections of random orders.
def make_rows(groups):
 r=sum(groups); blocks=[]; start=0
 for z in groups: blocks.append(set(range(start,start+z)));start+=z
 weight=r//2
 rows=[]
 for A in itertools.combinations(range(r),weight):
  A=set(A)
  if 0 in A and all(A&B and B-A for B in blocks): rows.append(A)
 assert len(rows)>=21
 rows=rows[:21]
 for A,B in itertools.combinations(rows,2): assert A&B and A-B and B-A and set(range(r))-A-B
 return rows,blocks
for groups in [(3,3,3),(3,3,2,2),(2,2,2,2,3),(2,2,2,2,2,2)]:
 rows,blocks=make_rows(groups);r=sum(groups);t=len(groups)
 words=list(range(8)); sig=[]
 for j in range(r):
  order=sorted(words,key=lambda w:tuple(((w>>(20-l))&1) if j in rows[l] else 1-((w>>(20-l))&1) for l in range(21)))
  sig.append({w:k for k,w in enumerate(order)})
 assert all(any(s[a]>s[b] and s[a]>s[c] for s in sig) for a,b,c in itertools.permutations(words,3))
 for block in blocks:
  assert all(any(sig[j][a]>sig[j][b] for j in block) for a,b in itertools.permutations(words,2))
 q=[(w,) for w in words]+list(itertools.combinations(words,2));qe=[set(x) for x in q]
 for trial in range(20):
  orders=[]
  for i in range(t):
   p=list(range(8));random.shuffle(p);orders.append({a:k for k,a in enumerate(p)})
  le=lambda a,b:all(o[a]<=o[b] for o in orders)
  elems=list(itertools.product(range(8),range(len(q))))
  keys=[]
  for j in range(r):
   i=next(i for i,b in enumerate(blocks) if j in b)
   keys.append([(max(sig[j][v] for v in q[A]),orders[i][p],len(q[A]),A) for p,A in elems])
  for a,(p,A) in enumerate(elems):
   for b,(p2,B) in enumerate(elems):
    target=le(p,p2) and qe[A]<=qe[B]
    got=all(k[a]<=k[b] for k in keys)
    assert target==got,(groups,trial,elems[a],elems[b])
 print('Independent audit passed',groups,'20 random P, all 82,944 ordered product pairs each')
