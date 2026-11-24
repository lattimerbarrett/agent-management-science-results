import itertools,random,pathlib

def rank2(rows):
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
random.seed(12345);count=0
for n in range(4,10):
 edges=list(itertools.combinations(range(n),2));idx={e:i for i,e in enumerate(edges)}
 triples=list(itertools.combinations(range(n),3))
 for trial in range(1000):
  g=random.getrandbits(len(edges))
  triangles=[t for t in triples if sum((g>>idx[e])&1 for e in itertools.combinations(t,2))%2]
  if len(triangles)==len(triples):continue
  boundaries=[sum(1<<idx[e] for e in itertools.combinations(t,2)) for t in triangles]
  h1=len(edges)-(n-1)-rank2(boundaries)
  assert h1>0
  # Explicit cocycle h is not a cut because its coboundary is nonzero somewhere
  h=g^((1<<len(edges))-1)
  assert all((h&b).bit_count()%2==0 for b in boundaries)
  assert any((h&sum(1<<idx[e] for e in itertools.combinations(t,2))).bit_count()%2 for t in triples)
  count+=1
print('two-graph H1 obstruction cases checked',count)
