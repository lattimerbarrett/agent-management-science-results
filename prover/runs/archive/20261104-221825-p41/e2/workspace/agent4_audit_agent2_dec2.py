import json,itertools,pathlib,functools
obj=json.load(open('workspace/agent2_terminal_dec2_certificate.json'));nodes=obj['nodes'];seen=set()
def maskset(m):return frozenset(i for i in range(m.bit_length()) if m>>i&1)
def powerset(S):
 L=list(S);return frozenset(frozenset(c) for r in range(len(L)+1) for c in itertools.combinations(L,r))
def maximal(C):return frozenset(x for x in C if not any(x<y for y in C))
@functools.lru_cache(None)
def audit(i):
 seen.add(i);node=nodes[i]
 if node[0]=='s':return powerset(maskset(node[1]))
 _,s,D,L=node;s=maskset(s);assert 1<=len(s)<=3
 deletion=audit(D);link=audit(L)
 assert all(not(s&G) for G in link)
 C=deletion|frozenset(H|G for H in powerset(s) for G in link)
 assert frozenset(G for G in C if not s<=G)==deletion
 assert frozenset(G-s for G in C if s<=G)==link
 fs=maximal(C);ds=maximal(deletion)
 assert len({len(F) for F in fs})==1
 assert {len(F) for F in ds}=={len(F) for F in fs}
 return C
C=audit(obj['root']);expected=frozenset(maskset(F) for F in json.load(open('workspace/agent2_blowup_candidate.json'))['facets'])
assert maximal(C)==expected
print('INDEPENDENT LITERAL-SET AUDIT PASS',len(seen),'reachable nodes',len(expected),'facets',len(C),'faces')
