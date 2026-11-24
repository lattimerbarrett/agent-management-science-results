import sys,pickle
sys.path.insert(0,'workspace')
from agent2_source_relations import generators
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form,smith_normal_form
from sympy.polys.domains import ZZ
from itertools import combinations

def standard(n):return [(i,j,k) for i in range(n) for j,k in combinations(range(n),2)]
def coords(n):
    labels=standard(n); inds={a:i for i,a in enumerate(labels)};G=generators(n); N=len(G)
    J=S.zeros(N,N)
    for col,g in enumerate(G):
        if g[0]=='C':
            _,i,j=g;a,b=sorted((i,j));sign=1 if j<i else -1
        else:_,i,a,b=g;sign=1
        J[inds[i,a,b],col]=sign
    assert J.T*J==S.eye(N)
    return J

def gl_action(n,A):
    L=standard(n);N=len(L);Ai=A.inv();T=S.zeros(N,N)
    for c,(i,a,b) in enumerate(L):
        for r,(q,j,k) in enumerate(L):
            T[r,c]=Ai[i,q]*(A[j,a]*A[k,b]-A[k,a]*A[j,b])
    J=coords(n)
    return J.T*T*J

def wedge2(T):
    P=list(combinations(range(T.rows),2));return S.Matrix([[T[i,a]*T[j,b]-T[i,b]*T[j,a] for a,b in P] for i,j in P])

def close_GL(n,H):
    actions=[]
    for a in range(n):
        for b in range(n):
            if a!=b:
                A=S.eye(n);A[a,b]=1;actions.append(wedge2(gl_action(n,A)))
    for it in range(10):
        B=hermite_normal_form(S.Matrix.hstack(H,*(T*H for T in actions)))
        print('closure',it,'shape',B.shape,flush=True)
        if B==H:break
        H=B
    else:raise Exception('not stable')
    D=smith_normal_form(H,domain=ZZ)
    ds=[D[i,i] for i in range(H.cols)]
    print('Smith',ds,flush=True)
    return H

def bracket_matrix(n):
    from agent2_low_degree_checks import add,bracket
    L=standard(n);J=coords(n);G=generators(n);N=len(G)
    ds=[]
    for c in range(N):
        D=[{} for i in range(n)]
        for r,(i,j,k) in enumerate(L):
            if J[r,c]:D[i]=add(D[i],bracket({(j,):1},{(k,):1}),int(J[r,c]))
        ds.append(D)
    def apply(D,w):
        ans={}
        for a in range(len(w)):
            for v,c in D[w[a]].items():
                u=w[:a]+v+w[a+1:];ans[u]=ans.get(u,0)+c
        return ans
    from itertools import product
    rows=[(i,w) for i in range(n) for w in product(range(n),repeat=3)]
    columns=[]
    for a,b in combinations(range(N),2):
        E=[{} for i in range(n)]
        for i in range(n):
            for w,c in ds[b][i].items():E[i]=add(E[i],apply(ds[a],w),c)
            for w,c in ds[a][i].items():E[i]=add(E[i],apply(ds[b],w),-c)
        columns.append([E[i].get(w,0) for i,w in rows])
    return S.Matrix.hstack(*(S.Matrix(c) for c in columns))

if __name__=='__main__':
    G,P,R,H=pickle.load(open('workspace/agent2_ia3_quadratic_relations.pkl','rb'))
    B=close_GL(3,H)
    J=bracket_matrix(3)
    assert J*B==S.zeros(J.rows,B.cols)
    assert J.rank()==18 and B.cols==18
    print('Verified primitive relation lattice equals degree2 Johnson kernel',flush=True)
    pickle.dump(B,open('workspace/agent2_ia3_GL_relations.pkl','wb'))
