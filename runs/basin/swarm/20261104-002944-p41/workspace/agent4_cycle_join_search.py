from itertools import combinations
from collections import defaultdict,Counter

def bsets(x,q):
    return [sum(c) for c in combinations([1<<i for i in range(x.bit_length()) if x>>i&1],q)]

def flips(fs):
    edges={e for f in fs for e in bsets(f,2)}
    triples=defaultdict(list)
    for f in fs:
        for t in bsets(f,3):triples[t].append(f)
    out=[]
    for t,inc in triples.items():
        if len(inc)!=2:continue
        uv=(inc[0]^t)|(inc[1]^t)
        if uv in edges:continue
        nxt=frozenset((set(fs)-set(inc))|{uv|e for e in bsets(t,2)})
        out.append(nxt)
    return out

def root(m,n):
    e1=[(1<<i)|(1<<((i+1)%m)) for i in range(m)]
    e2=[(1<<(m+i))|(1<<(m+(i+1)%n)) for i in range(n)]
    return frozenset(a|b for a in e1 for b in e2)

def score(fs,n):
    tr={t for f in fs for t in bsets(f,3)}
    return sum(sum(t in tr for t in bsets(f,3))>=3 for f in bsets((1<<n)-1,4) if f not in fs)

def main():
    states={root(4,4)}
    for level in range(5):
        print('level',level,'states',len(states),flush=True)
        if level==4:
            scores=Counter(score(fs,8) for fs in states)
            print('all neighborly sphere missing-tet attachment counts',dict(scores),flush=True)
            assert scores.get(0,0)==0
            alltet=set(bsets(255,4))
            for fs in states:
                cur=set(fs)
                while cur!=alltet:
                    tr={t for f in cur for t in bsets(f,3)}
                    nxt={f for f in alltet-cur if sum(t in tr for t in bsets(f,3))>=3}
                    assert nxt, ('stalled',fs,cur)
                    cur.update(nxt)
            print('All608 neighborly results bootstrap-close to all70 tetrahedra',flush=True)
            break
        states={nxt for fs in states for nxt in flips(fs)}
if __name__=='__main__':main()
