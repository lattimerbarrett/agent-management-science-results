"""Exact finite checks for the irreducible homogeneous low-rank lists.
This does NOT replace the geometric classification of uniform bundles.
Run with Python 3 (standard library only).
"""
from fractions import Fraction
from itertools import product, combinations

def sl_dimension(weight):
    n=len(weight)+1
    value=Fraction(1)
    for i in range(n):
        for j in range(i+1,n):
            value *= Fraction(sum(weight[i:j])+j-i,j-i)
    assert value.denominator == 1
    return value.numerator

def low_rank_irreps(n):
    # Each Dynkin coefficient a_i satisfies dim >= a_i+1. Thus
    # coefficients >=2*n-1 cannot have dimension <2*n.
    return {a:sl_dimension(a) for a in product(range(2*n-1),repeat=n-1)
            if sl_dimension(a)<2*n}

def line_exterior(splitting,p):
    return sorted((sum(t) for t in combinations(splitting,p)), reverse=True)

def main():
    expected={2:{(0,):1,(1,):2,(2,):3},
              3:{(0,0):1,(1,0):3,(0,1):3},
              4:{(0,0,0):1,(1,0,0):4,(0,1,0):6,(0,0,1):4}}
    for n in (2,3,4):
        actual=low_rank_irreps(n)
        assert actual==expected[n], (n,actual)
        print('SL_%d irreducibles of dimension < %d:'%(n,2*n),actual)
    # Euler sequence gives T_Pn|line=(2,1,...,1).
    for n in (2,3,4):
        tangent=[2]+[1]*(n-1)
        cotangent=[-x for x in tangent]
        assert len(tangent)==n and sum(tangent)==n+1
        print('P%d tangent splitting:'%n,tangent,
              '; cotangent splitting:',sorted(cotangent,reverse=True))
    assert line_exterior([2,1,1,1],2)==[3,3,3,2,2,2]
    # Sym^2 T_P2, including repeated basis weights.
    assert sorted([2+2,2+1,1+1],reverse=True)==[4,3,2]
    print('P2 Sym^2 T splitting:',[4,3,2])
    print('P4 exterior-square tangent splitting:',line_exterior([2,1,1,1],2))
    # Exterior-square quotient construction: rank C(n,2)-1 <2n.
    # A skew form on n+1 variables of rank >=6 requires n>=5.
    admissible=[n for n in range(2,101) if n*(n-1)//2-1<2*n and n+1>=6]
    assert admissible==[5]
    # Beyond n=100 inequality remains false since quadratic difference increases.
    assert 100*101//2-1-2*101>0
    print('Only dimension allowed by this construction:',admissible)
if __name__=='__main__': main()
