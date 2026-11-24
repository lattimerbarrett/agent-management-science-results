import sys,json,pickle,re,time
sys.path.insert(0,'workspace')
from agent2_source_relations import generators
from agent2_cubic_source import magnus3
from itertools import product
D=json.load(open('workspace/agent4_gap_ia4_data.json'));N=24;off=N*N;start=time.time()
names=[(g[0],)+tuple(map(int,re.findall(r'\d+',g))) for g in D['names']];index={g:i for i,g in enumerate(names)};oldG=generators(4);reindex=[]
for g in oldG:reindex.append(index[(g[0],)+tuple(x+1 for x in g[1:])])
class F2Lattice:
    def __init__(self):self.b={};self.queue=[]
    def insert(self,v):
        v=set(v)
        while v:
            p=min(v)
            if p in self.b:v.symmetric_difference_update(self.b[p])
            else:self.b[p]=v;self.queue.append(v);return True
        return False
    def reduce(self,v):
        v=set(v)
        for p,w in sorted(self.b.items()):
            if p in v:v.symmetric_difference_update(w)
        return v
L=F2Lattice();Q=pickle.load(open('workspace/agent2_rank4_quadratic_cubic.pkl','rb'))
for row in Q.values():
    v=set()
    for idx,c in row.items():
        if c%2:
            i,j,k=idx//(N*N),(idx//N)%N,idx%N;v.add(off+(reindex[i]*N+reindex[j])*N+reindex[k])
    L.insert(v)
print('Initialized Q3 mod2rank',len(L.b),'secs',time.time()-start,flush=True);L.queue=[]
def vector(p):
    v=set()
    for u,c in p.items():
        if not c%2:continue
        if len(u)==2:v.add(u[0]*N+u[1])
        if len(u)==3:v.add(off+(u[0]*N+u[1])*N+u[2])
    return v
for r in D['rels']:L.insert(vector(magnus3(tuple(r[::-1]),N)))
print('Added806seeds totalrank',len(L.b),'newqueue',len(L.queue),'secs',time.time()-start,flush=True)
operators=[]
for e in D['endomorphisms']:
    qs=[magnus3(tuple(w[::-1]),N) for w in e]
    lin=[{u[0] for u,c in q.items() if len(u)==1 and c%2} for q in qs]
    quad=[{u for u,c in q.items() if len(u)==2 and c%2} for q in qs]
    operators.append((lin,quad,{}))
def monomial(op,idx):
    lin,quad,cache=op
    if idx in cache:return cache[idx]
    v=set()
    def toggle(x):
        if x in v:v.remove(x)
        else:v.add(x)
    if idx<off:
        i,j=divmod(idx,N)
        for a,b in product(lin[i],lin[j]):toggle(a*N+b)
        for (a,b),c in product(quad[i],lin[j]):toggle(off+(a*N+b)*N+c)
        for a,(b,c) in product(lin[i],quad[j]):toggle(off+(a*N+b)*N+c)
    else:
        w=idx-off;i,j,k=w//off,w//N%N,w%N
        for a,b,c in product(lin[i],lin[j],lin[k]):toggle(off+(a*N+b)*N+c)
    cache[idx]=v;return v
idx=0
while idx<len(L.queue):
    v=L.queue[idx];idx+=1
    for op in operators:
        w=set()
        for i in v:w.symmetric_difference_update(monomial(op,i))
        L.insert(w)
    if idx%50==0:print('processed',idx,'queue',len(L.queue),'rank',len(L.b),'secs',time.time()-start,flush=True)
C={p-off:{i-off for i in v} for p,v in L.b.items() if p>=off}
a=index['M',3,1,2];b=index['M',1,2,3];c=index['C',1,2]
W={off+(a*N+b)*N+c,off+(b*N+a)*N+c,off+(c*N+a)*N+b,off+(c*N+b)*N+a}
res=L.reduce(W)
print('FINALrank4mixedmod2rank',len(L.b),'purecubicrank',len(C),'oldWremainder',len(res),'time',time.time()-start,flush=True)
pickle.dump(C,open('workspace/agent2_rank4_cubic_F2_source.pkl','wb'))
