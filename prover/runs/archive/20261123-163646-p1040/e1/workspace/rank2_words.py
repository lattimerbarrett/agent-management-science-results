from itertools import product
from pathlib import Path

def red(w):
    out=[]
    for a in w:
        if out and out[-1]==-a: out.pop()
        else: out.append(a)
    return tuple(out)
def inv(w): return tuple(-a for a in w[::-1])
def mul(*ws): return red(sum((tuple(w) for w in ws),()))
def apply(f,w): return mul(*(f[a-1] if a>0 else inv(f[-a-1]) for a in w))
def comp(f,g): return tuple(apply(f,w) for w in g)
def power(f,k):
    assert k>=0
    out=((1,),(2,))
    for _ in range(k): out=comp(out,f)
    return out
