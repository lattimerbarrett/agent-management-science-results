from fractions import Fraction as Q
from math import factorial, comb

def r2_shift_certificate():
    lam=Q(7,3)
    # All terms after l=4 are positive, so this finite sum certifies
    # sum_{l>=0} (l*(l-1)-1)*lam**l/(l!)**2 > 0 exactly.
    partial=sum((l*(l-1)-1)*lam**l/Q(factorial(l)**2) for l in range(5))
    assert partial==Q(16715,46656) and partial>0
    # Coefficientwise domination used in the dominated-convergence proof.
    reverse=[Q(1),Q(7),Q(9),Q(1)]
    upper=[comb(3,j)*lam**j for j in range(4)]
    assert all(x<=y for x,y in zip(reverse,upper))
    return partial, reverse, upper

if __name__=='__main__':
    print(r2_shift_certificate())
