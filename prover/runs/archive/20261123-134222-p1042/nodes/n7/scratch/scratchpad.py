import itertools as it
m=7
all_triangles=[];missing=[];verified=0
for cols in it.combinations(range(m),3):
 for rows in it.product(range(4),repeat=3):
  tri=tuple(zip(cols,rows));all_triangles.append(tri)
  if len(set(rows))==1:
   missing.append(tri)
   v=(next(c for c in range(m) if c not in cols),(rows[0]+1)%4)
   for edge in it.combinations(tri,2):
    t=edge+(v,)
    assert len({x[0] for x in t})==3
    assert max(sum(y==r for _,y in t) for r in range(4))<=2
   verified+=1
print('join triangles:',len(all_triangles))
print('missing triangles:',len(missing))
print('missing triangles with valid cone fillings:',verified)
print('For arbitrary m>=7, the identical construction applies, since every capacity is at least 2.')
