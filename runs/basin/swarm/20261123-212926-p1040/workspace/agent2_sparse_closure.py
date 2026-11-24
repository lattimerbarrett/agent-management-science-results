import sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_source_relations import generators,extend
from agent2_gl_closure import gl_action
from itertools import combinations
import sympy as S

class UnitLattice:
    def __init__(self):self.b={};self.queue=[];self.blocked=0
    def insert(self,v):
        v={i:int(c) for i,c in v.items() if c}
        while v:
            p=min(v);a=v[p]
            if p in self.b:
                w=self.b[p]
                for i,c in w.items():
                    t=v.get(i,0)-a*c
                    if t:v[i]=t
                    else:v.pop(i,None)
            else:
                if abs(a)!=1:self.blocked+=1;return False
                if a<0:v={i:-c for i,c in v.items()}
                self.b[p]=v;self.queue.append(v);return True
        return False

def action_maps(n):
    N=len(generators(n));P=list(combinations(range(N),2));pi={x:i for i,x in enumerate(P)}
    out=[]
    for p in range(n):
        for q in range(n):
            if p==q:continue
            A=S.eye(n);A[p,q]=1;T=gl_action(n,A)
            cols=[[(i,int(T[i,j])) for i in range(N) if T[i,j]] for j in range(N)]
            act=[]
            for i,j in P:
                v={}
                for a,x in cols[i]:
                    for b,y in cols[j]:
                        if a==b:continue
                        k=pi[min(a,b),max(a,b)];s=1 if a<b else -1
                        v[k]=v.get(k,0)+s*x*y
                act.append({k:c for k,c in v.items() if c})
            out.append(act)
    return out

def apply(act,v):
    ans={}
    for i,c in v.items():
        for j,d in act[i].items():
            t=ans.get(j,0)+c*d
            if t:ans[j]=t
            else:ans.pop(j,None)
    return ans

def seed(n,L):
    G=generators(n);gi={g:i for i,g in enumerate(G)};P=list(combinations(range(len(G)),2));pi={p:i for i,p in enumerate(P)}
    unit=tuple((i+1,) for i in range(n))
    for k,(i,j) in enumerate(P):
        if extend(extend(unit,G[i],1),G[j],1)==extend(extend(unit,G[j],1),G[i],1):L.insert({k:1})
    print('commuting rank',len(L.b),flush=True)
    G4,P4,R4,H4=pickle.load(open('workspace/agent2_ia4_quadratic_relations.pkl','rb'))
    H4=pickle.load(open('workspace/agent2_ia4_GL_relations.pkl','rb'))
    cols=[{i:int(H4[i,j]) for i in range(H4.rows) if H4[i,j]} for j in range(H4.cols)]
    for subset in combinations(range(n),4):
        ids=[]
        for g in G4:ids.append(gi[(g[0],)+tuple(subset[x] for x in g[1:])])
        emb={i:(pi[min(ids[a],ids[b]),max(ids[a],ids[b])],1 if ids[a]<ids[b] else -1) for i,(a,b) in enumerate(P4)}
        for col in cols:L.insert({emb[i][0]:c*emb[i][1] for i,c in col.items()})
    print('seed rank',len(L.b),'blocked',L.blocked,flush=True)

def run(n):
    start=time.time();L=UnitLattice();seed(n,L)
    acts=action_maps(n);print('actions ready',time.time()-start,flush=True)
    idx=0
    while idx<len(L.queue):
        v=L.queue[idx];idx+=1
        for act in acts:L.insert(apply(act,v))
        if idx%500==0:print('processed',idx,'rank',len(L.b),'blocked',L.blocked,'secs',time.time()-start,flush=True)
    N=n*n*(n-1)//2;target=N*(N-1)//2-(n*n*(n*n-1)//3-n*(n+1)//2)
    print('FINAL',n,'rank',len(L.b),'expected kernel',target,'blocked',L.blocked,'seconds',time.time()-start,flush=True)
    assert len(L.b)==target
    pickle.dump(L.b,open(f'workspace/agent2_ia{n}_sparse_relations.pkl','wb'))
    return L
def johnson_columns(n):
    G=generators(n);ds=[]
    for g in G:
        if g[0]=='C':_,i,j=g;ds.append((i,{(j,i):1,(i,j):-1}))
        else:_,i,j,k=g;ds.append((i,{(j,k):1,(k,j):-1}))
    def act(D,w):
        r,P=D;ans={}
        for a,x in enumerate(w):
            if x==r:
                for v,c in P.items():
                    u=w[:a]+v+w[a+1:];ans[u]=ans.get(u,0)+c
        return ans
    cols=[]
    for a,b in combinations(range(len(G)),2):
        v={}
        for D,E,s in [(ds[a],ds[b],1),(ds[b],ds[a],-1)]:
            root,P=E
            for w,c in P.items():
                for u,d in act(D,w).items():
                    idx=root*n**3+u[0]*n*n+u[1]*n+u[2]
                    v[idx]=v.get(idx,0)+s*c*d
        cols.append({i:c for i,c in v.items() if c})
    return cols

def certify(n,L):
    cols=johnson_columns(n);I=UnitLattice()
    for c in cols:I.insert(c)
    N=n*n*(n-1)//2
    assert len(I.b)+len(L.b)==N*(N-1)//2
    for rel in L.b.values():
        image={}
        for i,c in rel.items():
            for j,d in cols[i].items():image[j]=image.get(j,0)+c*d
        assert not any(image.values())
    print('CERTIFIED',n,'relation rank',len(L.b),'Johnson rank',len(I.b),'source quotient injects integrally',flush=True)

if __name__=='__main__':
    for n in [2,3,4]:
        L=UnitLattice()
        for c in johnson_columns(n):L.insert(c)
        assert len(L.b)==n*n*(n*n-1)//3-n*(n+1)//2
        print('Primitive bracket image',n,'rank',len(L.b),'blocked',L.blocked,flush=True)
    for n in [5,6]:certify(n,run(n))
