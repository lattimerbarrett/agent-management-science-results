import itertools,json,collections
cores=[set(range(4*i,4*i+4)) for i in range(6)];F=cores[0]|{4,24};data=[];counts=collections.Counter()
for owner in range(6):
 for y in range(24):
  if y in cores[owner]:continue
  G=cores[owner]|{y,24}
  if F&G!={24}:continue
  assert owner in [2,3,4,5]
  oy=y//4;case='same_foreign_core' if oy==1 else 'new_foreign_core'
  assert oy==1 or oy in set(range(2,6))-{owner}
  cm={0:0,1:1,owner:2}
  if case=='new_foreign_core':cm[oy]=3
  for a,b in zip(sorted(set(range(6))-set(cm)),sorted(set(range(6))-set(cm.values()))):cm[a]=b
  perm={24:24}
  for a,b in cm.items():
   domain=sorted(cores[a]);image=sorted(cores[b])
   special={}
   if a==1:special[4]=4
   if a==oy:special[y]=5 if case=='same_foreign_core' else 12
   perm.update(special)
   for x,z in zip([v for v in domain if v not in special],[v for v in image if v not in special.values()]):perm[x]=z
  assert set(perm)==set(range(25)) and set(perm.values())==set(range(25))
  assert {perm[v] for v in F}==F
  rep=cores[2]|{24,5 if case=='same_foreign_core' else 12}
  assert {perm[v] for v in G}==rep
  assert all({perm[v] for v in cores[a]}==cores[b] for a,b in cm.items())
  counts[case]+=1;data.append(dict(owner=owner,y=y,case=case,permutation=[perm[v] for v in range(25)]))
assert counts==dict(same_foreign_core=12,new_foreign_core=48)
out=dict(F=sorted(F),counts=dict(counts),total=len(data),witnesses=data)
json.dump(out,open('workspace/agent4_private_external_pair_orbits.json','w'));open('workspace/agent4_private_external_pair_orbits.py','w').write(open(__file__).read());print(dict(counts),'total',len(data))
open('workspace/agent4_private_external_pair_orbits.txt','w').write('''Private-external-pair symmetry lemma for rank6, cover6, six cores of size4, one external point p=24.\nEvery point z of every member F is private against some member E: F is itself a cover of size6 (intersecting), while F minus z has size5 and cannot cover. Thus E intersects F exactly at z.\nAfter anchoring F=X0+{4,p}, choose its private witness for p, G. Then G must contain p, cannot own core0 (it would share X0), and cannot own core1 (it would share4). Hence its owner lies in {2,3,4,5}; its other petalpoint y lies outside X0, that owncore, and {4,p}. It either lies in X1 minus4, or in one of the three other unanchored cores. The stabilizer of F and the core partition has exactly two orbits, represented by G=X2+{p,5} and G=X2+{p,12}. Python explicitly enumerates all60 possibilities and supplies a genuine core-preserving permutation fixing F to the stated representative: orbit sizes12 and48.\nTherefore testing the two anchored branches is complete, not heuristic. The lemma does not decide either branch, and does not address configurations with more external vertices.\n''')
