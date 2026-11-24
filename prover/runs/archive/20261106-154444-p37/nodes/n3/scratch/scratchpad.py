import itertools
# Explicit two-colour flat representation with d=5, n=13.
a=3;d=a+2
proper=list(range(1,(1<<a)-1))
ups=[]
for bits in range(1<<len(proper)):
 U={proper[i] for i in range(len(proper)) if bits>>i&1}
 if all(y in U for x in U for y in proper if x&y==x):ups.append(U)
# Representatives of complementary pairs are {coordinate 0} union B.
# The coordinate-1 side is determined by complementarity.
perms=[]
for j in range(d):
 def key(U):
  return tuple(int(B in U) if (j==0 or (j>=2 and B>>(j-2)&1)) else int(B not in U) for B in proper)
 perms.append(sorted(range(len(ups)),key=lambda v:key(ups[v])))
pos=[{v:i for i,v in enumerate(p)} for p in perms]
N=len(ups)
suitable=all(any(all(pos[j][v]>pos[j][w] for w in T if w!=v) for j in range(d)) for T in itertools.combinations(range(N),3) for v in T)
flat=all(any(pos[j][v]>pos[j][w] for j in G) for v in range(N) for w in range(N) if v!=w for G in [(0,1),tuple(range(2,d))])
print('number of available vertices:',N)
print('3-suitable:',suitable)
print('both coordinate blocks provide a flat coordinate at every incidence:',flat)
