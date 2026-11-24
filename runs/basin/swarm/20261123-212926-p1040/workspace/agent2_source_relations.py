from itertools import combinations
from collections import Counter
from math import gcd
import sympy as S
from sympy.matrices.normalforms import smith_normal_form, hermite_normal_form
from sympy.polys.domains import ZZ

def red(w):
    st=[]
    for x in w:
        if st and st[-1]==-x:st.pop()
        else:st.append(x)
    return tuple(st)
def inv(w):return tuple(-i for i in w[::-1])
def cat(*words):return red(x for w in words for x in w)
def cm(a,b):return cat(a,b,inv(a),inv(b))
def generators(n):
    out=[]
    for i in range(n):
        for j in range(n):
            if i!=j:out.append(('C',i,j))
        for j,k in combinations(range(n),2):
            if i not in (j,k):out.append(('M',i,j,k))
    return out

def extend(A,g,s):
    typ,i,*args=g
    B=list(A)
    if typ=='C':
        j=args[0]; v=A[j] if s==1 else inv(A[j]);B[i]=cat(v,A[i],inv(v))
    else:
        j,k=args;v=cm(A[j],A[k]);B[i]=cat(A[i],v if s==1 else inv(v))
    return tuple(B)

def lattice_relations(n=3,depth=4):
    G=generators(n);N=len(G)
    pairs=list(combinations(range(N),2));pidx={p:i for i,p in enumerate(pairs)};M=len(pairs)
    unit=tuple((i+1,) for i in range(n))
    z=(0,)*N; zz=(0,)*M
    seen={unit:(z,zz,())}; layer=[(unit,z,zz,())]
    rels={}; found=Counter()
    for d in range(1,depth+1):
        nxt=[]
        for A,e,c,w in layer:
            for a,g in enumerate(G):
                for s in (1,-1):
                    letter=s*(a+1)
                    if w and w[-1]==-letter:continue
                    B=extend(A,g,s)
                    f=list(e); f[a]+=s; f=tuple(f)
                    v=list(c)
                    for j in range(a+1,N):v[pidx[a,j]]-=s*e[j]
                    v=tuple(v); ww=w+(letter,)
                    if B in seen:
                        f0,v0,w0=seen[B]
                        assert f0==f
                        rel=tuple(x-y for x,y in zip(v,v0))
                        if any(rel):
                            if next(x for x in rel if x)<0:rel=tuple(-x for x in rel); ww,w0=w0,ww
                            if rel not in rels:rels[rel]=(ww,w0);found[d]+=1
                    else:
                        seen[B]=(f,v,ww);nxt.append((B,f,v,ww))
        layer=nxt
        R=S.Matrix(list(rels)).T if rels else S.zeros(M,0)
        print('depth',d,'seen',len(seen),'layer',len(layer),'relations',len(rels),'rank',R.rank(),flush=True)
    R=S.Matrix(list(rels)).T
    H=hermite_normal_form(R)
    D=smith_normal_form(H,domain=ZZ)
    elementary=[D[i,i] for i in range(min(D.shape))]
    print('relation rank',H.cols,'Smith invariants',elementary,flush=True)
    return G,pairs,rels,H

if __name__=='__main__':
    import pickle
    G,pairs,rels,H=lattice_relations(depth=5)
    with open('workspace/agent2_ia3_quadratic_relations.pkl','wb') as f:pickle.dump((G,pairs,rels,H),f)
