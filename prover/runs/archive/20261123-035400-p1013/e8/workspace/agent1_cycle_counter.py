from fractions import Fraction
from math import factorial, comb
from functools import lru_cache

@lru_cache(None)
def _part_poly(N, mandatory):
    ans=[Fraction(0)]*(N+1)
    if mandatory==0: ans[0]=Fraction(1)
    for j in range(1,N+1):
        ans[j]=sum((Fraction(comb(N-mandatory,k-mandatory)*factorial(k)*(-1)**(k-j)*comb(k-1,j-1),factorial(j)) for k in range(max(j,mandatory),N+1)),Fraction(0))
    return tuple(ans)

@lru_cache(None)
def _cross_pseudo(parts, mandatory=0):
    """All multipartite cycles containing specified mandatory vertices of first part;
    includes length-two cycles weighted 1/2 (needed for path contractions)."""
    if mandatory>parts[0]: return Fraction(0)
    poly=[Fraction(1)]
    for i,N in enumerate(parts):
        a=_part_poly(N,mandatory if i==0 else 0)
        out=[Fraction(0)]*(len(poly)+len(a)-1)
        for j,x in enumerate(poly):
            for k,y in enumerate(a): out[j+k]+=x*y
        poly=out
    # log determinant contains spurious single-color terms; remove all of them.
    total=sum((factorial(j-1)*poly[j] for j in range(2,len(poly))),Fraction(0))/2
    for i,N in enumerate(parts):
        if mandatory and i!=0: continue
        a=_part_poly(N,mandatory if i==0 else 0)
        total-=sum((factorial(j-1)*a[j] for j in range(2,len(a))),Fraction(0))/2
    return total

def star_forest_cycles(parts, star_degrees=()):
    """Exact cycles in complete multipartite graph + disjoint stars in first part.
    star_degrees lists leaf-counts of all stars, isolated vertices implicit."""
    parts=tuple(parts)
    if sum(d+1 for d in star_degrees)>parts[0]: raise ValueError('stars do not fit')
    coeff={(0,0):1}
    for d in star_degrees:
        new={}
        for (p,e),v in coeff.items():
            for dp,de,w in [(0,0,1),(1,1,d),(1,2,comb(d,2))]:
                new[p+dp,e+de]=new.get((p+dp,e+de),0)+v*w
        coeff=new
    ans=Fraction(0)
    for (p,e),v in coeff.items():
        ans+=v*2**p*_cross_pseudo((parts[0]-e,)+parts[1:],p)
    ans-=Fraction(sum(parts[i]*parts[j] for i in range(len(parts)) for j in range(i)),2)
    assert ans.denominator==1
    return int(ans)


def internal_component_cycles(parts, components):
    """components: (vertex_count, {(path_components,edge_count):count}, cycles)
    for disjoint internal graphs in first part. Dictionary enumerates all spanning
    subsets of internal edges of maximum degree<=2 containing no cycles.
    Isolated vertices are implicit. Internal simple cycles must be counted separately.
    """
    parts=tuple(parts)
    assert sum(v for v,_,_ in components)<=parts[0]
    coeff={(0,0):1}
    for _,a,_ in components:
        new={}
        for (p,e),v in coeff.items():
            for (q,f),w in a.items():
                new[p+q,e+f]=new.get((p+q,e+f),0)+v*w
        coeff=new
    ans=sum(c for _,_,c in components)
    for (p,e),v in coeff.items():
        ans+=v*2**p*_cross_pseudo((parts[0]-e,)+parts[1:],p)
    ans-=Fraction(sum(parts[i]*parts[j] for i in range(len(parts)) for j in range(i)),2)
    assert ans.denominator==1
    return int(ans)

def star(d):
    return (d+1,{(0,0):1,(1,1):d,(1,2):comb(d,2)},0)

def path(d):
    a={(0,0):1}
    for e in range(1,d+1):
        for p in range(1,min(e,d-e+1)+1):
            a[p,e]=comb(e-1,p-1)*comb(d-e+1,p)
    return (d+1,a,0)

def triangle():
    return (3,{(0,0):1,(1,1):3,(1,2):3},1)


@lru_cache(None)
def _cross_pseudo_multi(parts, mandatory):
    if any(q>N for q,N in zip(mandatory,parts)): return Fraction(0)
    poly=[Fraction(1)]
    for N,q in zip(parts,mandatory):
        a=_part_poly(N,q)
        out=[Fraction(0)]*(len(poly)+len(a)-1)
        for j,x in enumerate(poly):
            for k,y in enumerate(a):out[j+k]+=x*y
        poly=out
    total=sum((factorial(j-1)*poly[j] for j in range(2,len(poly))),Fraction(0))/2
    for i,(N,q) in enumerate(zip(parts,mandatory)):
        if any(z for j,z in enumerate(mandatory) if j!=i):continue
        a=_part_poly(N,q)
        total-=sum((factorial(j-1)*a[j] for j in range(2,len(a))),Fraction(0))/2
    return total

def multipartite_component_cycles(parts, components_by_part):
    """Exact cycles, arbitrary disjoint internal components in every part."""
    from itertools import product
    assert len(parts)==len(components_by_part)
    polys=[]
    answer=Fraction(sum(c for cs in components_by_part for _,_,c in cs))
    for N,components in zip(parts,components_by_part):
        assert sum(v for v,_,_ in components)<=N
        coeff={(0,0):1}
        for _,a,_ in components:
            new={}
            for (p,e),v in coeff.items():
                for (q,f),w in a.items():new[p+q,e+f]=new.get((p+q,e+f),0)+v*w
            coeff=new
        polys.append(coeff)
    for choices in product(*(list(a.items()) for a in polys)):
        mandatory=tuple(t[0][0] for t in choices)
        edges=tuple(t[0][1] for t in choices)
        multiplicity=1
        for _,v in choices:multiplicity*=v
        contracted=tuple(n-e for n,e in zip(parts,edges))
        answer+=multiplicity*2**sum(mandatory)*_cross_pseudo_multi(contracted,mandatory)
    answer-=Fraction(sum(parts[i]*parts[j] for i in range(len(parts)) for j in range(i)),2)
    assert answer.denominator==1
    return int(answer)
