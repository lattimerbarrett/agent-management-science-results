"""Exact free-group / truncated-Magnus arithmetic; no external executables."""
from itertools import product
from collections import defaultdict

def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)

def inverse_word(w): return tuple(-x for x in reversed(w))
def commutator_word(u,v): return reduce_word(tuple(u)+tuple(v)+inverse_word(u)+inverse_word(v))
def substitute(w, images):
    out=()
    for x in w:
        image=images[abs(x)-1]
        out=reduce_word(out+(image if x>0 else inverse_word(image)))
    return out

def add(a,b,scale=1):
    out=dict(a)
    for w,c in b.items():
        out[w]=out.get(w,0)+scale*c
        if not out[w]: del out[w]
    return out

def mul(a,b,degree):
    out=defaultdict(int)
    for u,c in a.items():
        for v,d in b.items():
            if len(u)+len(v)<=degree: out[u+v]+=c*d
    return {w:c for w,c in out.items() if c}

def inverse(a,degree):
    assert a.get((),0)==1
    q=add(a,{():1},-1)
    out={():1}; power={():1}
    for k in range(1,degree+1):
        power=mul(power,q,degree)
        out=add(out,power,(-1)**k)
    return out

def magnus(w,degree):
    out={():1}
    for x in w:
        image={():1,(abs(x),):1}
        if x<0: image=inverse(image,degree)
        out=mul(out,image,degree)
    return out

def homogeneous(a,d): return {w:c for w,c in a.items() if len(w)==d}
def bracket(a,b):
    if not a or not b: return {}
    d=max(map(len,a))+max(map(len,b))
    return add(mul(a,b,d),mul(b,a,d),-1)

def homogeneous_centralizer_matrix(n,d):
    """P -> ([P,X_1],...,[P,X_n]) on homogeneous associative tensors."""
    import sympy as sp
    words=list(product(range(1,n+1),repeat=d))
    target=list(product(range(1,n+1),repeat=d+1))
    rows={(i,w):i*len(target)+j for i in range(n) for j,w in enumerate(target)}
    M=sp.zeros(n*len(target),len(words))
    for j,w in enumerate(words):
        for i in range(n):
            M[rows[i,w+(i+1,)],j]+=1
            M[rows[i,(i+1,)+w],j]-=1
    return M
