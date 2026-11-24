"""Self-contained exact certificate verification of the lower-bound example.
Uses only Python's standard library. Bit masks represent faces.
"""
from itertools import combinations
from functools import lru_cache
from collections import Counter

TRACE = [4103, 13313, 821248, 5123, 66563, 65603, 65634, 65571, 99, 559106, 296962, 819202, 38914, 36870, 526850, 526912, 65543, 898, 532738, 4131, 135202, 131234, 137248, 133154, 6178, 67618, 329730, 327746, 328706, 10274, 262466, 68098, 305, 8234, 787458, 787488, 786442, 4138, 263216, 113, 4110, 66051, 98817, 328720, 344080, 8206, 33297, 295440, 294978, 336896, 393744, 74241, 16465, 16457, 8721, 147536, 147528, 263696, 352256, 614400, 139792, 16968, 550912, 16906, 26656, 549120, 205312, 729088, 606224, 540689, 17026, 17088, 319488, 16577, 17537, 139408, 204928, 540801, 544769, 73864, 542721, 788481, 57600, 50432, 99584, 790529, 663808, 395265, 18437, 589848, 172288, 172160, 165120, 18441, 41096, 19457, 524314, 4385, 4392, 6432, 2352, 2448, 6528, 4122, 69656, 69704, 4172, 18468, 2340, 262436, 786468, 786692, 524580, 804, 525060, 524836, 263204, 525348, 787460, 8290, 8514, 4896, 4992, 525408, 1136, 263178, 5130, 787464, 525384, 5192, 525322]

def subs(f):
    g=f
    while True:
        yield g
        if not g:return
        g=(g-1)&f

def faces(F): return frozenset(g for f in F for g in subs(f))
def maximal(S):
    S=set(S)
    return tuple(sorted(f for f in S if not any(f!=g and f&g==f for g in S)))
def delete(F,s): return tuple(f for f in F if f&s!=s)
def link(F,s): return tuple(sorted(f^s for f in F if f&s==s))

@lru_cache(None)
def vertex_certificate(F):
    if len(F)==1:return ('simplex',F[0])
    if not F:return None
    r=F[0].bit_count()
    if any(f.bit_count()!=r for f in F):return None
    ridges=Counter(f^(1<<v) for f in F for v in range(f.bit_length()) if f>>v&1)
    V=0
    for f in F:V|=f
    for v in range(V.bit_length()):
        s=1<<v
        if not V&s:continue
        C=[f for f in F if f&s]
        D=delete(F,s)
        if not D or any(ridges[f^s]==1 for f in C):continue
        dc=vertex_certificate(D)
        if dc is None:continue
        lc=vertex_certificate(link(F,s))
        if lc is not None:return ('shed',s,dc,lc)
    return None

# This deliberately verifies the definition using ALL faces, independently
# of the ridge-multiplicity shortcut used in the certificate search.
def verify(F,k,c):
    assert c is not None and F
    S=faces(F)
    r=F[0].bit_count()
    assert all(f.bit_count()==r for f in F)
    if c[0]=='simplex':
        assert F==(c[1],)
        return 1
    _,s,dc,lc=c
    assert s in S and 1<=s.bit_count()<=k+1
    D=maximal(g for g in S if g&s!=s)
    L=maximal(g for g in S if not g&s and (g|s) in S)
    assert D and all(g.bit_count()==r for g in D)
    return 1+verify(D,k,dc)+verify(L,k,lc)

def boundary_extend(F,f,c):
    S=faces(F)
    assert f not in S and all(g in S for g in subs(f) if g!=f)
    if f.bit_count()==1:
        return ('shed',f,c,('simplex',0))
    assert c[0]=='shed'
    _,s,dc,lc=c
    if f&s==s:
        return ('shed',s,dc,boundary_extend(link(F,s),f^s,lc))
    return ('shed',s,boundary_extend(delete(F,s),f,dc),lc)

def facet_order(F,c):
    if c[0]=='simplex':return list(F)
    _,s,dc,lc=c
    return facet_order(delete(F,s),dc)+[s|g for g in facet_order(link(F,s),lc)]

def appendable(F,f):
    I=maximal(f&g for g in F)
    return bool(I) and all(g.bit_count()==f.bit_count()-1 for g in I)

def base_facets():
    # Staircase triangulation of the explicitly triangulated corridor disk x I.
    P=[4,5,6];Q=[7,8,9];disk=[]
    for apex,path in [(0,[2]+P+[3]),(1,[2]+Q+[3])]:
        disk.extend(tuple(sorted((apex,a,b))) for a,b in zip(path,path[1:]))
    disk.extend([(2,4,7),(3,6,9)])
    for i in range(2):
        disk.extend([(P[i],P[i+1],Q[i+1]),(P[i],Q[i],Q[i+1])])
    out=[]
    for t in disk:
        a,b,c=sorted(t)
        out.extend([(a,b,c,c+10),(a,b,b+10,c+10),(a,a+10,b+10,c+10)])
    return tuple(sorted(sum(1<<v for v in f) for f in out))

B=base_facets()
assert len(B)==42
basecert=vertex_certificate(B)
verify(B,0,basecert)
baseorder=facet_order(B,basecert)
for i in range(1,len(baseorder)+1):
    P=tuple(sorted(baseorder[:i]))
    verify(P,0,vertex_certificate(P))

# The final eight moves are commuted so that each triangle-restriction
# move extends the currently active edge-shedding block.
permutation=list(range(123))+[125,126,127,130,123,124,128,129]
assert sorted(permutation)==list(range(131))
F=B;c=basecert;current_edge=None;counts=Counter()
for i in permutation:
    f=TRACE[i];S=faces(F)
    assert f not in S and appendable(F,f)
    R=sum(1<<v for v in range(20) if f>>v&1 and (f^(1<<v)) in S)
    counts[R.bit_count()]+=1
    if R.bit_count()==2:
        current_edge=R
        c=('shed',R,c,('simplex',f^R))
    elif R.bit_count()==3:
        assert current_edge is not None and R&current_edge==current_edge
        assert c[0]=='shed' and c[1]==current_edge
        L=link(tuple(sorted(F+(f,))),current_edge)
        c=('shed',current_edge,c[2],vertex_certificate(L))
    else:
        assert R.bit_count()==4
        c=boundary_extend(F,f,c)
    F=tuple(sorted(F+(f,)))
    verify(F,1,c)

assert len(F)==173 and len(set(F))==173
S=faces(F)
assert [sum(g.bit_count()==j for g in S) for j in range(5)]==[1,20,190,337,173]
missing=[]
for q in combinations(range(20),4):
    f=sum(1<<v for v in q)
    if f not in S:
        assert not appendable(F,f)
        missing.append(f)
assert len(missing)==4672
boundaries=[]
for q in combinations(range(20),5):
    f=sum(1<<v for v in q)
    if all((f^(1<<v)) in S for v in q):boundaries.append(f)
assert len(boundaries)==7
print('VERIFIED: 20 vertices, 173 facets; k=1 certificate nodes:',verify(F,1,c))
print('All 131 extension certificates verified; restriction counts:',dict(counts))
print('All 4672 missing tetrahedra blocked; seven old 5-set boundaries:',boundaries)
