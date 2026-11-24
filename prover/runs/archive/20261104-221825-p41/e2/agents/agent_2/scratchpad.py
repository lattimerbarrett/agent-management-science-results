import json
source=open('workspace/agent2_terminal_dec2_verify.py').read()
K=json.load(open('workspace/agent2_hornfree_tree.json'));T=[sum(1<<i for i in t) for t in K['triangles']]
M=json.load(open('workspace/agent2_orbit_shelling.json'))['markers'];codes=[]
for q in M:codes.append(sum(1<<i for i in q[1:]) if q[0]=='e' else sum(1<<i for i in q[1:4])+256*(q[-1]+1))
old="O=json.load(open('workspace/agent2_blowup_best_shelling.json'))['order'];k=2"
new=f'''TRIANGLES={T!r}
MARKERS={codes!r}
priority={{x:i for i,x in enumerate(MARKERS)}}
O=[]
for f in itertools.combinations(range(16),4):
    counts=[sum(v//2==i for v in f) for i in range(8)]
    origins=sum(1<<i for i in range(8) if counts[i])
    if origins.bit_count()==2:
        marker=origins
    elif origins in TRIANGLES:
        p=next(i for i in range(8) if counts[i]==2)
        marker=origins+256*(p+1)
    else:continue
    O.append((priority[marker],f))
O=[sum(1<<v for v in f) for _,f in sorted(O)]
assert len(O)==280
k=2
'''
assert old in source;source=source.replace(old,new)
source=source[:source.index("json.dump({'k':k")]
source+='''
# Literal subset/maximal-intersection verification of every forbidden first step.
old=set().union(*(set(subs(f)) for f in O))
assert set(i for f in O for i in range(16) if f>>i&1)==set(range(16))
blocked=0
for vertices in itertools.combinations(range(16),4):
    F=sum(1<<v for v in vertices)
    if F in O:continue
    intersection=[s for s in subs(F) if s in old]
    maximal=[s for s in intersection if not any(t!=s and s&t==s for t in intersection)]
    assert any(s.bit_count()<3 for s in maximal)
    blocked+=1
assert blocked==1540
print('All 1540 missing tetrahedra blocked; b(3,2)>=1, contrary to requested value 0.')
'''
open('workspace/agent2_selfcontained_counterexample.py','w').write(source)
exec(source)
