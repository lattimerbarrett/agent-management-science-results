"""Exact reduced-word and truncated integral Magnus computations.
No numerical linear algebra or inferred identities.  Words use signed 1-based letters.
"""
from collections import defaultdict

def reduce_word(w):
    out=[]
    for a in w:
        if out and out[-1]==-a: out.pop()
        else: out.append(a)
    return tuple(out)

def inverse(w): return tuple(-a for a in reversed(w))
def product(*ws): return reduce_word(a for w in ws for a in w)
def substitute(w, images):
    return product(*(images[a-1] if a>0 else inverse(images[-a-1]) for a in w))
def compose(f,g): return tuple(substitute(w,f) for w in g)
def auto_commutator(f,fi,g,gi): return compose(compose(compose(f,g),fi),gi)
def word_commutator(u,v): return product(u,v,inverse(u),inverse(v))
def identity(n): return tuple((i,) for i in range(1,n+1))
def multiply(a,b,degree):
    out=defaultdict(int)
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)<=degree: out[u+v]+=x*y
    return {w:c for w,c in out.items() if c}
def magnus(w,degree):
    out={():1}
    for a in w:
        i=abs(a)
        factor={():1,(i,):1} if a>0 else {(i,)*k:(-1)**k for k in range(degree+1)}
        out=multiply(out,factor,degree)
    return out

def johnson_terms(images,degree):
    """Return Magnus expansions of f(x_i)x_i^-1, less constant 1, through degree."""
    out=[]
    for i,w in enumerate(images,1):
        q=magnus(product(w,(-i,)),degree)
        q.pop((),None)
        out.append(q)
    return tuple(out)
def is_andreadakis(images,r):
    """Exact test f in A_r, assuming images define an automorphism.
    Magnus dimension theorem over Z: w in gamma_(r+1) iff terms <=r vanish.
    """
    return not any(johnson_terms(images,r))
def K(n,i,j):
    f=list(identity(n)); f[i-1]=(j,i,-j)
    fi=list(identity(n)); fi[i-1]=(-j,i,j)
    return tuple(f),tuple(fi)
def C(n,i,j,k):
    f=list(identity(n)); h=word_commutator((j,),(k,)); f[i-1]=product((i,),h)
    fi=list(identity(n)); fi[i-1]=product((i,),inverse(h))
    return tuple(f),tuple(fi)

def self_test():
    for n in range(2,6):
        gens=[]
        for i in range(1,n+1):
            for j in range(1,n+1):
                if i!=j: gens.append(K(n,i,j))
            for j in range(1,n+1):
                for k in range(j+1,n+1):
                    if i not in (j,k): gens.append(C(n,i,j,k))
        for f,fi in gens:
            assert compose(f,fi)==compose(fi,f)==identity(n)
            assert is_andreadakis(f,1) and not is_andreadakis(f,2)
        # Every pair is checked, not sampled.
        for f,fi in gens:
            for g,gi in gens:
                h=auto_commutator(f,fi,g,gi)
                assert is_andreadakis(h,2)
        print('n=',n,'generators=',len(gens),'pair-commutators checked=',len(gens)**2)
    # A genuine nonzero degree-two Johnson image.
    f,fi=K(3,1,2); g,gi=K(3,2,3)
    h=auto_commutator(f,fi,g,gi)
    assert not is_andreadakis(h,3)
    print('nonzero degree-two leading terms:',johnson_terms(h,3))
if __name__=='__main__': self_test()
