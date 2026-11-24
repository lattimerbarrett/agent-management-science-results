from itertools import combinations
from z3 import Solver, Bool, Or, Not, sat, is_true
import time, pickle

def covers(edges,limit=5,maxout=200):
    edges=sorted(set(edges),key=int.bit_count)
    out=[]; seen=set()
    def dfs(c):
        if c in seen or len(out)>=maxout:return
        seen.add(c)
        if any(c&d==d for d in out):return
        missing=next((e for e in edges if not e&c),None)
        if missing is None:
            for b in list(bits(c)):
                d=c^(1<<b)
                if all(d&e for e in edges):c=d
            out.append(c);return
        if c.bit_count()==limit:return
        for b in bits(missing):dfs(c|(1<<b))
    dfs(0)
    return out

def bits(m):
    while m:
        b=m&-m; yield b.bit_length()-1; m-=b

def check(t=6,r=2,k=6,extra=2,kind='external'):
    start=time.time(); size=k-r; n=t*size+extra
    blocks=[set(range(i*size,(i+1)*size)) for i in range(t)]
    edges=[]; groups=[]
    for i,X in enumerate(blocks):
        xm=sum(1<<x for x in X); ids=[]
        for R in combinations([x for x in range(n) if x not in X],r):
            ids.append(len(edges));edges.append(xm|sum(1<<x for x in R))
        groups.append(ids)
    s=Solver();s.set(timeout=30000)
    vs=[Bool('e%d'%j) for j in range(len(edges))]
    for ids in groups:s.add(Or([vs[j] for j in ids]))
    for i,E in enumerate(edges):
        for j in range(i):
            if not E&edges[j]:s.add(Or(Not(vs[i]),Not(vs[j])))
    base=sum(1<<x for x in blocks[0])
    if kind=='external':base|=(1<<(n-1))|(1<<(n-2))
    elif kind=='mixed':base|=(1<<(n-1))|(1<<min(blocks[1]))
    elif kind=='same':base|=(1<<min(blocks[1]))|(1<<(min(blocks[1])+1))
    elif kind=='different':base|=(1<<min(blocks[1]))|(1<<min(blocks[2]))
    s.add(vs[edges.index(base)])
    print('setup',k,extra,kind,n,len(edges),time.time()-start,flush=True)
    done=set()
    for iteration in range(2000):
        ans=s.check()
        if ans!=sat:
            print('result',str(ans),'iteration',iteration,'seconds',time.time()-start,flush=True);return
        m=s.model(); chosen=[j for j,v in enumerate(vs) if is_true(m.eval(v))]
        bad=covers([edges[j] for j in chosen],t-1)
        if not bad:
            data=dict(t=t,k=k,extra=extra,blocks=blocks,edges=[edges[j] for j in chosen])
            pickle.dump(data,open('example.pkl','wb'))
            print('FOUND',len(chosen),data,flush=True);return
        for c in bad:
            if c not in done:
                s.add(Or([vs[j] for j,e in enumerate(edges) if not e&c]));done.add(c)
        if iteration%10==0:print(iteration,len(chosen),len(bad),len(done),round(time.time()-start,1),flush=True)
    print('iteration limit')
check(extra=2,kind='external')
