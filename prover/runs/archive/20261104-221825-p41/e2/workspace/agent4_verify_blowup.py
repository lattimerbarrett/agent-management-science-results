import json,itertools,pathlib
cand=json.load(open('workspace/agent2_blowup_candidate.json'));order=json.load(open('workspace/agent2_blowup_best_shelling.json'))['order'];n=cand['n'];facets=cand['facets']
assert len(order)==len(set(order))==len(facets)==280
assert set(order)==set(facets)
assert all(f.bit_count()==4 for f in facets)
assert __import__('functools').reduce(int.__or__,facets)==(1<<n)-1

def maximal_intersections(F,old):
 ints={F&G for G in old}
 return sorted(x for x in ints if not any(x!=y and x&y==x for y in ints))
for i,F in enumerate(order):
 if i==0:continue
 mx=maximal_intersections(F,order[:i])
 if not mx or any(g.bit_count()!=3 for g in mx):
  print('SHELLING FAIL',i,F,mx,flush=True);raise SystemExit
print('SHELLING ALL280 VERIFIED BY DIRECTMAXIMAL INTERSECTIONS',flush=True)
blocked=0;good=[];witness=[]
for c in itertools.combinations(range(n),4):
 F=sum(1<<v for v in c)
 if F in facets:continue
 mx=maximal_intersections(F,facets)
 if mx and all(g.bit_count()==3 for g in mx):good.append(F)
 else:blocked+=1;witness.append([F,mx])
print('missing blocked',blocked,'appendable',good,flush=True)
json.dump({'shelling_verified':True,'blocked':blocked,'appendable':good,'maximal_intersections':witness},open('workspace/agent4_blowup_independent_verification.json','w'))
