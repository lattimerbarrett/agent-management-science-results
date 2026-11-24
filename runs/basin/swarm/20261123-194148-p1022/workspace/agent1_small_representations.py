from fractions import Fraction
from itertools import product

def weyl_dimension(labels):
    n = len(labels)+1
    lam = [sum(labels[i:]) for i in range(n-1)] + [0]
    d = Fraction(1)
    for i in range(n):
        for j in range(i+1,n):
            d *= Fraction(lam[i]-lam[j]+j-i,j-i)
    assert d.denominator == 1
    return int(d)

def small_representations(n, bound):
    # Weyl dimension is monotone in each nonnegative Dynkin label.
    # A label >=bound has dimension >=bound+1 (already its simple-root factor).
    return [(a,weyl_dimension(a)) for a in product(range(bound),repeat=n-1)
            if weyl_dimension(a)<=bound]

if __name__ == '__main__':
    expected = {
       2: [((0,),1),((1,),2),((2,),3)],
       3: [((0,0),1),((0,1),3),((1,0),3)],
       4: [((0,0,0),1),((0,0,1),4),((0,1,0),6),((1,0,0),4)]}
    for n in (2,3,4):
        result = small_representations(n,2*n-1)
        assert result == expected[n], (n,result)
        print('P%d rank<=%d: %s' % (n,2*n-1,result))
    print('This checks only small Levi representation dimensions, NOT the classification of uniform bundles.')
