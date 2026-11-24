import sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_source_relations import generators,extend,inv
from agent2_sparse_closure import UnitLattice
from agent2_gl_closure import gl_action
from itertools import combinations,product
import sympy as S

class IntegralLattice:
    def __init__(self):self.b={};self.queue=[];self.blocked=0
    def insert(self,v):
        v={i:int(c) for i,c in v.items() if c}
        changed=False
        while v:
            p=min(v);a=v[p]
            if p not in self.b:
                if a<0:v={i:-c for i,c in v.items()}
                self.b[p]=v;self.queue.append(v);return True
            w=self.b[p];d=w[p];q=a//d
            for i,c in w.items():
                t=v.get(i,0)-q*c
                if t:v[i]=t
                else:v.pop(i,None)
            if v.get(p,0):
                # Euclidean exchange: preserve old pivot row as next remainder.
                self.b[p]=v;self.queue.append(v);v=w;changed=True
        return changed

def magnus3(word,N):
    p={():1}
    for x in word:
        a=abs(x)-1; terms=[((),1),((a,),1)] if x>0 else [(tuple([a]*k),(-1)**k) for k in range(4)]
        q={}
        for u,c in p.items():
            for v,d in terms:
                if len(u)+len(v)<=3:q[u+v]=q.get(u+v,0)+c*d
        p={u:c for u,c in q.items() if c}
    return p

def compose(A,B):
    from agent2_source_relations import cat
    Ai=[inv(w) for w in A]
    return tuple(cat(*(A[x-1] if x>0 else Ai[-x-1] for x in w)) for w in B)

def cubic_sources(depth=4):
    n=3;G=generators(n);N=len(G);off=N*N
    unit=tuple((i+1,) for i in range(n));seen={unit:()};layer=[(unit,())];L=IntegralLattice(); count=0
    from agent2_source_relations import cat
    targets={};found={}
    for a in range(n):
        for b in range(n):
            if a==b:continue
            U=list(unit);Ui=list(unit);U[b]=cat(unit[b],unit[a]);Ui[b]=cat(unit[b],inv(unit[a]));U=tuple(U);Ui=tuple(Ui)
            for k,g in enumerate(G):
                target=compose(compose(U,extend(unit,g,1)),Ui)
                targets.setdefault(target,[]).append((a,b,k))
    for d in range(1,depth+1):
        nxt=[]
        for A,w in layer:
            for a,g in enumerate(G):
                for s in (1,-1):
                    letter=s*(a+1)
                    if w and w[-1]==-letter:continue
                    B=extend(A,g,s);ww=w+(letter,)
                    if B not in seen:
                        seen[B]=ww;nxt.append((B,ww))
                        if B in targets:
                            for label in targets[B]:found[label]=ww
                        continue
                    w0=seen[B]
                    if ww==w0:continue
                    p=magnus3(ww+inv(w0),N)
                    assert not any(len(u)==1 for u in p)
                    v={}
                    for u,c in p.items():
                        if len(u)==2:v[u[0]*N+u[1]]=c
                        if len(u)==3:v[off+(u[0]*N+u[1])*N+u[2]]=c
                    L.insert(v);count+=1
        layer=nxt
        print('depth',d,'seen',len(seen),'relations tested',count,'lattice rank',len(L.b),'pure cubic',sum(p>=off for p in L.b),'blocked',L.blocked,flush=True)
    print('Found Nielsen conjugate lifts',len(found),'of54; lengths',sorted(set(map(len,found.values()))),flush=True)
    pickle.dump(found,open('workspace/agent2_nielsen_lifts.pkl','wb'))
    pickle.dump(L.b,open('workspace/agent2_ia3_mixed_relations.pkl','wb'))
    C=IntegralLattice()
    for p,v in L.b.items():
        if p>=off:C.insert({i-off:c for i,c in v.items()})
    # Full known quadratic relation lattice gives valid cubic commutator rels.
    H=pickle.load(open('workspace/agent2_ia3_GL_relations.pkl','rb'));P=list(combinations(range(N),2))
    for col in range(H.cols):
        p={}
        for r,(i,j) in enumerate(P):
            c=int(H[r,col])
            if c:p[(i,j)]=c;p[(j,i)]=-c
        for k in range(N):
            v={}
            for (i,j),c in p.items():
                a=(i*N+j)*N+k;b=(k*N+i)*N+j
                v[a]=v.get(a,0)+c;v[b]=v.get(b,0)-c
            C.insert(v)
    print('cubic plus quadratic consequences',len(C.b),'blocked',C.blocked,flush=True)
    return C

def tensor_actions(n=3):
    N=len(generators(n));out=[]
    for a in range(n):
        for b in range(n):
            if a==b:continue
            A=S.eye(n);A[a,b]=1;T=gl_action(n,A);col=[[(i,int(T[i,j])) for i in range(N) if T[i,j]] for j in range(N)]
            act=[]
            for i,j,k in product(range(N),repeat=3):
                v={}
                for x,c in col[i]:
                    for y,d in col[j]:
                        for z,e in col[k]:v[(x*N+y)*N+z]=c*d*e
                act.append(v)
            out.append(act)
    # Include determinant-minus-one inversion, not merely SL3.
    A=S.eye(n);A[0,0]=-1;T=gl_action(n,A)
    diag=[int(T[i,i]) for i in range(N)]
    out.append([{(i*N+j)*N+k:diag[i]*diag[j]*diag[k]} for i,j,k in product(range(N),repeat=3)])
    return out

def run():
    start=time.time();C=cubic_sources(depth=5);actions=tensor_actions();idx=0
    from agent2_sparse_closure import apply
    while idx<len(C.queue):
        v=C.queue[idx];idx+=1
        for act in actions:C.insert(apply(act,v))
    print('FINAL CUBIC RELATION RANK',len(C.b),'pivot values',sorted(set(v[p] for p,v in C.b.items())),'blocked',C.blocked,'secs',time.time()-start,flush=True)
    from sympy.matrices.normalforms import smith_normal_form
    from sympy.polys.domains import ZZ
    M=S.zeros(729,len(C.b))
    for j,v in enumerate(C.b.values()):
        for i,c in v.items():M[i,j]=c
    D=smith_normal_form(M,domain=ZZ)
    diag=[abs(D[i,i]) for i in range(len(C.b))]
    print('Smith invariant values',sorted(set(diag)),flush=True)
    from collections import Counter
    print('Smith counts',dict(Counter(diag)),flush=True)
    pickle.dump(C.b,open('workspace/agent2_ia3_cubic_relations.pkl','wb'))
    return C
if __name__=='__main__':run()
