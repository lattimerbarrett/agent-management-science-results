import itertools as it,json
from pathlib import Path
examples=[(2,[{0,1},{2}],[0,1],[{frozenset({0,1})},{frozenset({0,2}),frozenset({1,2})}]),(3,[{0,1},{2,3},{4,5}],[1,1,1],[{frozenset({0,1,x}) for x in [2,3]},{frozenset({2,3,x}) for x in [4,5]},{frozenset({4,5,x}) for x in [0,1]}])]
results=[]
for t,cores,d,classes in examples:
 H=set().union(*classes);V=set().union(*H);C=[frozenset(S) for S in it.combinations(V,t) if all(set(S)&E for E in H)]
 assert all(any(not set(S)&E for E in H) for S in it.combinations(V,t-1))
 for v,w in it.combinations(V,2):assert any({v,w}<=S for S in C)
 candidates=0
 for i,X in enumerate(cores):
  for q in range(d[i]+1):
   for P in it.combinations(V-X,q):
    E=frozenset(X|set(P));candidates+=1
    if all(E&F for F in H):assert E in H
 exhausted=[S for S in C if any(X<=S for X in cores)];assert all(S in H for S in exhausted)
 assert all(S&T for S,T in it.combinations(exhausted,2))
 results.append({'t':t,'cost':sum(d),'ground':len(V),'members':len(H),'minimum_covers':len(C),'all_pairs_checked':len(V)*(len(V)-1)//2,'all_rank_budget_candidates':candidates,'core_exhausting_minimum_covers':len(exhausted)})
Path('workspace/agent2_saturated_global_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_saturated_global_checks.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
