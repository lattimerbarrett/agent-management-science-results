from collections import defaultdict
from pathlib import Path

def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)
def inverse(w): return tuple(-x for x in reversed(w))
def comm(u,v): return reduce_word(u+v+inverse(u)+inverse(v))
def triple(i,j,k): return comm(comm((i,),(j,)),(k,))
def power(w,k): return (w if k>=0 else inverse(w))*abs(k)

# Alphabet 1=a, 2=b, 3=m, 4=d, 5=e.
u=reduce_word(power(triple(1,5,3),3)+power(triple(1,3,5),-1)
              +power(triple(1,2,2),-4)+power(triple(2,3,4),-2))
assert len(u)==92

def add(p,q,scale=1):
    out=defaultdict(int,p)
    for w,c in q.items(): out[w]+=scale*c
    return {w:c for w,c in out.items() if c}
def multiply(p,q):
    out=defaultdict(int)
    for v,a in p.items():
        for w,b in q.items():
            if len(v)+len(w)<=4: out[v+w]+=a*b
    return {w:c for w,c in out.items() if c}
def magnus(w):
    out={():1}
    for x in w:
        if x>0: factor={():1,(x,):1}
        else: factor={(abs(x),)*j:(-1)**j for j in range(5)}
        out=multiply(out,factor)
    return out

spec=[('K',1,2),('K',1,3),('M',1,2,3),('K',2,1),('M',2,1,3)]
def generator_images(g,sign):
    typ,i,*jk=spec[g-1]
    images=[{(j,):1} for j in (1,2,3)]
    if typ=='K':
        j=jk[0]; word=(sign*j,i,-sign*j)
    else:
        j,k=jk; h=(j,k,-j,-k)
        word=(h if sign>0 else inverse(h))+(i,)
    images[i-1]=add(magnus(word),{():1},-1)
    return images
G={s*g:generator_images(g,s) for g in range(1,6) for s in (-1,1)}
def substitute(p,images):
    out={}
    for w,c in p.items():
        term={():c}
        for j in w: term=multiply(term,images[j-1])
        out=add(out,term)
    return out
images=[{(j,):1} for j in (1,2,3)]
for g in reversed(u): images=[substitute(p,G[g]) for p in images]
assert images==[{(j,):1} for j in (1,2,3)]

# Literal Fox-target word, not just its leading Lie polynomial.
reflection_images=['B','A','AB','C','AC']
reflection_word=''.join(reflection_images[abs(g)-1][::1 if g>0 else -1] for g in u)
# Set of monomials = polynomial over F2; adjacent squares vanish.
poly={()}
for letter in reflection_word:
    new=set(poly)
    for w in poly:
        if len(w)<3 and (not w or w[-1]!=letter):
            v=w+(letter,)
            if v in new: new.remove(v)
            else: new.add(v)
    poly=new
assert poly=={(),tuple('ACB'),tuple('CAB'),tuple('BAC'),tuple('BCA')}
print('92-letter source word fixes all generators through Magnus degree 4.')
print('Target mod I^4: 1 + ACB + CAB + BAC + BCA (nonzero).')
import numpy as np
I=np.eye(4,dtype=np.int64)
A=I.copy(); A[0,1]=1
B=I.copy(); B[2,3]=1
C=I.copy(); C[1,2]=1
T=I.copy()
for letter in reflection_word:T=(T@{'A':A,'B':B,'C':C}[letter])%2
expected=I.copy();expected[0,3]=1
assert np.array_equal(T,expected)
print('Finite target UT4(F2):',T.tolist())
