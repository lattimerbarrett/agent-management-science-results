"""Finite combinatorial and arithmetic checks for the moment-curve lower bound.

The analytic compactness and polynomial-root arguments are in the proof;
these functions check the finite sign-pattern and dimension calculations.
"""
from itertools import product

STATES = tuple(product((-1, 1), repeat=2))

def min_roots_for_all_four():
    # A root of one affine polynomial permits one bit to change; simultaneous
    # roots permit two, at cost two. Every state must occur on an open interval.
    # Delete repeated states. A shortest path visiting all four is simple:
    # any repeats may be removed without increasing Hamming length.
    from itertools import permutations
    costs = []
    for order in permutations(STATES):
        cost = sum(sum(x != y for x,y in zip(a,b))
                   for a,b in zip(order,order[1:]))
        costs.append(cost)
    assert min(costs) == 3
    return min(costs)

def check_lower_bound(s):
    assert isinstance(s, int) and s >= 3
    j = 2**s - 2
    conjectured_lower = (3*j + 1)//2
    d = conjectured_lower - 1
    roots_needed = min_roots_for_all_four() * j
    roots_available = 2*d
    assert roots_available < roots_needed
    assert conjectured_lower == 3*2**(s-1)-3
    return dict(s=s, measures=j, lower_bound=conjectured_lower,
                excluded_dimension=d, required_roots=roots_needed,
                available_roots=roots_available)

if __name__ == '__main__':
    for s in range(3, 11):
        print(check_lower_bound(s))
