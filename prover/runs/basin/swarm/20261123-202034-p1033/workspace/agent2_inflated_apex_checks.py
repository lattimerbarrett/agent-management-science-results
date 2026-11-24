from pathlib import Path
import itertools as it,json
# Fano lines in XOR model nonzero vectors F_2^3.
B={frozenset({a+2,b+2,(a^b)+2}) for a in range(1,8) for b in range(a+1,8)}
assert len(B)==7 and all(len(Q)==3 for Q in B)
X=set(range(3,10));old=[{frozenset({0,1})},{frozenset({0,2}),frozenset({1,2})}];classes=[{F|Q for F in cl for Q in B} for cl in old]+[{frozenset(X)}];H=set().union(*classes);V=set(range(10));t=3
assert all(F&G for F,G in it.combinations(H,2))
assert all(any(not set(C)&F for F in H) for C in it.combinations(V,t-1))
Covers=[frozenset(C) for C in it.combinations(V,t) if all(set(C)&F for F in H)]
assert len(Covers)==28
assert all(any({v,w}<=C for C in Covers) for v,w in it.combinations(V,2))
assert all(any({v,w}<=C for C in Covers) for v,w in it.combinations(X,2))
# Uniformization only needs private core extension here: class ranks5,5,7.
private=[{10,11},{12,13},set()];unif=[{F|private[j] for F in cl} for j,cl in enumerate(classes)];UH=set().union(*unif);UV=set(range(14))
assert all(len(F)==7 for F in UH)
assert all(F&G for F,G in it.combinations(UH,2))
assert all(any(not set(C)&F for F in UH) for C in it.combinations(UV,t-1))
UC=[frozenset(C) for C in it.combinations(UV,t) if all(set(C)&F for F in UH)]
assert all(any({v,w}<=C for C in UC) for v,w in it.combinations(X,2))
result={'generalized_ground':len(V),'family_size':len(H),'minimum_covers':len(Covers),'all_pairs_mincover_complete':True,'uniform_k':7,'uniform_ground':len(UV),'uniform_minimum_covers':len(UC),'uniform_apex_used_size':len(X),'uniform_deficits':[3,4,0]}
Path('workspace/agent2_inflated_apex_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_inflated_apex_checks.json').write_text(json.dumps(result,indent=2));print(result)
