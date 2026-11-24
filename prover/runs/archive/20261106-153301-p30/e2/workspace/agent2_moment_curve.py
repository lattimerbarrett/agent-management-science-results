"""Exact checks for the standard two-hyperplane moment-curve lower bound.
No numerical solver and no assertion of the unproved extra dimension.
"""
from fractions import Fraction

def parameters(s):
    assert s >= 3
    j = 2**s - 2
    m = j//2
    d = 3*m
    return j,m,d

def roots(s):
    j,m,d=parameters(s)
    A,B=[],[]
    for k in range(j):
        a,b = (A,B) if k < m else (B,A)
        a.extend([4*k+1,4*k+3]); b.append(4*k+2)
    assert len(A)==len(B)==d
    assert len(set(A+B))==3*j
    return A,B

def polynomial_sign(roots,t):
    # All polynomials are monic; exact sign without expanding coefficients.
    assert t not in roots
    return -1 if sum(t<r for r in roots)%2 else 1

def verify(s):
    j,m,d=parameters(s)
    A,B=roots(s)
    for k in range(j):
        states=[]
        for q in range(4):
            t=Fraction(8*k+2*q+1,2)
            states.append((polynomial_sign(A,t),polynomial_sign(B,t)))
        assert len(set(states))==4
    # In dimension d-1, total possible roots falls short of the necessary
    # three transitions on each of j intervals.
    assert 2*(d-1)<3*j
    # Critical dimension has equality, not the extra-dimensional lower bound.
    assert 2*d==3*j
    return {'s':s,'j':j,'critical_dimension':d,'proposed_dimension':d+1,
            'checked_quarter_intervals':4*j}

if __name__=='__main__':
    for s in range(3,10): print(verify(s))
