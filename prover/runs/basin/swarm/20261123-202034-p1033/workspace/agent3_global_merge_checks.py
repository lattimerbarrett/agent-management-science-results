from itertools import combinations
from pathlib import Path
import json

def covers(H):
 V=set.union(*H)
 for s in range(len(V)+1):
  C=[set(C) for C in combinations(sorted(V),s) if all(set(C)&E for E in H)]
  if C:return s,C

def check_merges(H,cores):
 tau,B=covers(H);records=[]
 for v,w in combinations(sorted(set.union(*H)),2):
  owners=[next((i for i,X in enumerate(cores) if a in X),None) for a in (v,w)]
  if owners[0] is not None and owners[1] is not None and owners[0]!=owners[1]:continue
  HH=[{v if x==w else x for x in E} for E in H]
  newtau,_=covers(HH)
  criterion=any({v,w}<=C for C in B)
  assert (newtau<tau)==criterion
  assert newtau in (tau,tau-1)
  records.append(dict(pair=[v,w],tau_new=newtau,pair_in_mincover=criterion))
 return records

cores=[{0,1,2},{3,4}]
H=[set(cores[0])]+[set(cores[1])|{v} for v in cores[0]]
R=check_merges(H,cores)
assert len(R)==4 and all(a['tau_new']==2 for a in R)
J=json.load(open('workspace/agent3_fano_pruning_checks.json'))
FH=[set(E) for Fi in J['classes'] for E in Fi]
FR=check_merges(FH,[{i} for i in range(3)])
assert len(FR)==18 and all(a['tau_new']==2 for a in FR)
Path('workspace/agent3_global_merge_checks.json').write_text(json.dumps(dict(preserving_example=R,fano_dropping_example=FR),indent=2))
print('Verified',len(R),'preserving and',len(FR),'dropping generalized pair merges.')
