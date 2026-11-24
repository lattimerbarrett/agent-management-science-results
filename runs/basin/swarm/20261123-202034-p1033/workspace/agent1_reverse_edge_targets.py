from pathlib import Path
src=Path('workspace/agent3_factored_reverse_checks.py').read_text();src=src[:src.index('rows=[];')]
exec(src)
import z3,itertools,json,time

def bl(qs):
    ans={0}
    for q in qs:
        nxt={a for a in ans if a&q}
        for a in ans:
            if a&q: continue
            for p in range(q.bit_length()):
                if q>>p&1:nxt.add(a|(1<<p))
        order=sorted(nxt,key=int.bit_count);ans=set()
        for a in order:
            if not any(b&a==b for b in ans):ans.add(a)
    return ans

rows=[]
for t in [3,4]:
    X,H,owner,Q,N,n=example(t);qm=[sum(1<<p for p in q) for q in Q]
    fam=[]
    for x in range(n):
        a=bl([q for f,q in zip(H,qm) if x in f]);b=bl([q for f,q in zip(H,qm) if x not in f]);fam.append(sorted(a|{p|(1<<N) for p in b}))
    vertices=[(i,a) for i,fs in enumerate(fam) for a in fs]
    print('instance',t,'innern',n,'H',len(H),'outerfamilies',list(map(len,fam)),'vertices',len(vertices),flush=True)
    so=z3.Solver();so.set(timeout=120000)
    opts=[z3.Int('o_%s'%i) for i in range(len(vertices))]
    for o in opts:so.add(o>=0,o<len(H))
    cons=0
    for u,(i,a) in enumerate(vertices):
        for v in range(u):
            j,b=vertices[v]
            if i==j or a&b:continue
            choices=[opts[u]==e for e,f in enumerate(H) if j in f]+[opts[v]==e for e,f in enumerate(H) if i in f]
            so.add(z3.Or(choices));cons+=1
    start=time.time();res=so.check();row=dict(t=t,inner_n=n,inner_edges=len(H),outervertices=len(vertices),disjointconstraints=cons,result=str(res),secs=time.time()-start)
    if res==z3.sat:
        m=so.model();choices=[m[o].as_long() for o in opts]
        for u,(i,a) in enumerate(vertices):
            for v,(j,b) in enumerate(vertices[:u]):
                if i!=j and not a&b:assert j in H[choices[u]] or i in H[choices[v]]
        row['verified']=True;row['choices']=choices
    print(row,flush=True);rows.append(row)
Path('workspace/agent1_reverse_edge_targets.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent1_reverse_edge_targets.py').write_text(Path('scratchpad.py').read_text())
