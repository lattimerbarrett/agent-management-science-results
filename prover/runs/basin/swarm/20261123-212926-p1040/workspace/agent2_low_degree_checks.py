"""Independent finite checks for low-degree facts used in the Andreadakis problem.
Run with Python. Uses exact integer/rational arithmetic only.
These tests corroborate, and do not replace, the general mathematical arguments.
"""
from itertools import product
from math import prod
import sympy as S

def add(a,b,scale=1):
    c=dict(a)
    for w,v in b.items():
        c[w]=c.get(w,0)+scale*v
        if not c[w]: del c[w]
    return c

def mul(a,b,N):
    c={}
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)<=N:
                w=u+v;c[w]=c.get(w,0)+x*y
    return {w:v for w,v in c.items() if v}

def bracket(a,b):
    N=max(map(len,a),default=0)+max(map(len,b),default=0)
    return add(mul(a,b,N),mul(b,a,N),-1)

def magnus(word,N):
    a={():1}
    for k in word:
        i=abs(k)-1
        b={():1,(i,):1} if k>0 else {tuple([i]*d):(-1)**d for d in range(N+1)}
        a=mul(a,b,N)
    return a

def inverse(word):return tuple(-x for x in word[::-1])
def comm(u,v):return tuple(u)+tuple(v)+inverse(u)+inverse(v)

def johnson1(image,i):
    a=magnus(tuple(image)+(-i,),2)
    return {w:v for w,v in a.items() if len(w)==2}

def check_magnus_generators(n):
    # Basis coordinate is (input, ordered pair a<b).
    labels=[(i,a,b) for i in range(1,n+1) for a in range(1,n+1) for b in range(a+1,n+1)]
    columns=[]
    for i in range(1,n+1):
        for j in range(1,n+1):
            if j==i:continue
            im=(j,i,-j)
            d=johnson1(im,i)
            columns.append([d.get((a-1,b-1),0) if k==i else 0 for k,a,b in labels])
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                if i in (j,k):continue
                im=(i,)+comm((j,),(k,))
                d=johnson1(im,i)
                columns.append([d.get((a-1,b-1),0) if q==i else 0 for q,a,b in labels])
    M=S.Matrix.hstack(*(S.Matrix(c) for c in columns))
    assert M.rows==M.cols==n*n*(n-1)//2
    # In fact a signed permutation matrix, so no expensive determinant needed.
    assert all(sum(abs(M[i,j]) for i in range(M.rows))==1 for j in range(M.cols))
    assert all(sum(abs(M[i,j]) for j in range(M.cols))==1 for i in range(M.rows))
    return M.rows

def lyndon(w):return bool(w) and all(w<w[i:] for i in range(1,len(w)))

def lie_word(w):
    assert lyndon(w)
    if len(w)==1:return {w:1}
    for i in range(1,len(w)):
        if lyndon(w[i:]):
            return bracket(lie_word(w[:i]),lie_word(w[i:]))
    raise AssertionError

def check_center(n,d):
    W=[w for w in product(range(n),repeat=d) if lyndon(w)]
    bases=[lie_word(w) for w in W]
    witt=sum(int(S.mobius(k))*n**(d//k) for k in S.divisors(d))//d
    assert len(W)==witt
    rows=[(i,w) for i in range(n) for w in product(range(n),repeat=d+1)]
    cols=[]
    for b in bases:
        images=[bracket(b,{(i,):1}) for i in range(n)]
        cols.append([images[i].get(w,0) for i,w in rows])
    A=S.Matrix.hstack(*(S.Matrix(v) for v in cols))
    assert A.rank()==len(W)
    return len(W)

if __name__=='__main__':
    for n in range(2,8):
        print('Johnson1 signed basis',n,check_magnus_generators(n))
    for n,maxdegree in [(2,7),(3,4)]:
        for d in range(1,maxdegree+1):
            print('zero free-Lie center',n,d,check_center(n,d))
