import json,itertools
O=json.load(open('workspace/agent2_blowup_best_shelling.json'))['order'];k=2
nodes=[];cache={}
def simplex(F):
 key=('s',F)
 if key not in cache:cache[key]=len(nodes);nodes.append(key)
 return cache[key]
def split(s,D,L):
 key=('d',s,D,L)
 if key not in cache:cache[key]=len(nodes);nodes.append(key)
 return cache[key]
def full_add(N,F):
 node=nodes[N]
 assert node[0]=='d',('fullboundaryon simplex impossible',node,F)
 _,s,D,L=node
 if s&F==s:
  tau=F^s
  assert 1<=tau.bit_count()<=k+1
  return split(s,D,split(tau,L,simplex(0)))
 return split(s,full_add(D,F),L)
def subs(F):
 s=F
 while True:
  yield s
  if not s:return
  s=(s-1)&F
root=simplex(O[0]);faces=set(subs(O[0]))
for F in O[1:]:
 R=0
 for v in range(16):
  if F>>v&1 and F^(1<<v) in faces:R|=1<<v
 assert R not in faces
 if R.bit_count()<=k+1:root=split(R,root,simplex(F^R))
 else:
  assert R==F and all(s in faces for s in subs(F) if s!=F)
  root=full_add(root,F)
 faces.update(subs(F))
# Independent tree verifier from recursive definition, no shelling shortcuts.
verified={}
def verify(N):
 if N in verified:return verified[N]
 node=nodes[N]
 if node[0]=='s':answer=frozenset([node[1]])
 else:
  _,s,D,L=node;DF=verify(D);LF=verify(L)
  assert 1<=s.bit_count()<=k+1
  assert all(not(s&g) for g in LF)
  assert all(f&s!=s for f in DF)
  SF={s|g for g in LF};answer=frozenset(set(DF)|SF)
  sizes={f.bit_count() for f in answer};assert len(sizes)==1
  assert {f.bit_count() for f in DF}==sizes
  for F in SF:
   for v in range(16):
    if s>>v&1:
     H=F^(1<<v)
     assert any(H&g==H for g in DF),(N,s,F,H)
 verified[N]=answer
 return answer
assert verify(root)==frozenset(O)
print('EXPLICIT2DECOMPOSITION VERIFIED','nodes',len(nodes),'reachable',len(verified),'facets',len(O),'root',root,flush=True)
json.dump({'k':k,'root':root,'nodes':nodes},open('workspace/agent2_terminal_dec2_certificate.json','w'))
open('workspace/agent2_terminal_dec2_verify.py','w').write(open(__file__).read())
