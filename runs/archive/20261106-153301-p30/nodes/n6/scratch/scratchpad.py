# Substitute into the standard upper bound:
# Delta(2^q + r, k) <= 2^(q+k-1) + r,
# q >= 0, 1 <= r <= 2^q.
for s in range(3,9):
    j=2**s-2
    q=s-1
    r=j-2**q
    assert 1 <= r <= 2**q
    bound=2**(q+2-1)+r
    print(f's={s}, j={j}, q={q}, r={r}, upper={bound}, claimed expression={3*2**(s-1)-2}')
import sympy as sp
A=sp.symbols('A') # A = 2^(s-1)
print('Symbolic upper bound:', sp.expand(2*A+(A-2)))