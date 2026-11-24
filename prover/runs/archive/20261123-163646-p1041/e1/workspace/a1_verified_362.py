import json
ms=[3373,13010,13665,9585,7213]
def pts(mask):
 p=[0]
 for i in range(14):
  if mask>>i&1:p +=[x^(1<<i) for x in p]
 return p
flats=[pts(mask) for mask in ms]
flats[1]=[x^(((x>>4)&1)<<2) for x in flats[1]]
s=set()
for p in flats:s.symmetric_difference_update(p)
assert len(s)==362
projection={x>>7 for p in flats for x in p}
assert len(projection)==34
# Every flat is 7-dimensional: check linear span size128.
for p in flats:
 assert len(set(p))==128 and 0 in p
 rows=[]
 for x in p:
  for r in rows:x=min(x,x^r)
  if x:rows.append(x);rows.sort(reverse=True)
 assert len(rows)==7
# Independently recover full truth table ANF and verify degree7.
a=bytearray(1<<14)
for x in s:a[x]=1
for j in range(14):
 for x in range(1<<14):
  if x>>j&1:a[x]^=a[x^(1<<j)]
assert max(x.bit_count() for x,c in enumerate(a) if c)==7
print('362 seed independently verified; occupied parallel-flat cosets:',len(projection))
open('workspace/a1_verified_362.py','w').write(open(__file__).read())