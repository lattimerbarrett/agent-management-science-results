from pathlib import Path
src=Path('workspace/agent1_reverse_edge_targets.py').read_text();src=src[:src.index('\nrows=[]\n')];exec(src)
rows=[]
for t in [3,4]:
    X,H,owner,Q,N,n=example(t);qm=[sum(1<<p for p in q) for q in Q]
    fam=[]
    for x in range(n):
        a=bl([q for f,q in zip(H,qm) if x in f]);b=bl([q for f,q in zip(H,qm) if x not in f]);fam.append(sorted(a|{p|(1<<N) for p in b}))
    vertices=[(i,a) for i,fs in enumerate(fam) for a in fs]
    so=z3.Solver();so.set(timeout=120000)
    target=[[z3.Bool(f'x{u}_{j}') for j in range(n)] for u in range(len(vertices))]
    for u,(i,a) in enumerate(vertices):so.add(z3.Not(target[u][i]))
    cons=0
    for u,(i,a) in enumerate(vertices):
        for v in range(u):
            j,b=vertices[v]
            if i==j or a&b:continue
            so.add(z3.Or(target[u][j],target[v][i]));cons+=1
    for budget in range(1,n):
        so.push()
        for row in target:so.add(z3.PbLe([(x,1) for x in row],budget))
        start=time.time();res=so.check();entry=dict(t=t,n=n,vertices=len(vertices),ground=N+1,disjointpairs=cons,budget=budget,result=str(res),secs=time.time()-start)
        if res==z3.sat:
            m=so.model();sets=[{j for j in range(n) if z3.is_true(m.eval(v))} for row in target for v in []]
            sets=[{j for j,v in enumerate(row) if z3.is_true(m.eval(v))} for row in target]
            assert max(map(len,sets))<=budget
            for u,(i,a) in enumerate(vertices):
                for v,(j,b) in enumerate(vertices[:u]):
                    if i!=j and not a&b:assert j in sets[u] or i in sets[v]
            entry['verified']=True;entry['targets']=[sorted(x) for x in sets]
        print({k:v for k,v in entry.items() if k!='targets'},flush=True);rows.append(entry)
        so.pop()
        if res==z3.sat:break
Path('workspace/agent1_reverse_min_targets.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent1_reverse_min_targets.py').write_text(Path('scratchpad.py').read_text())
