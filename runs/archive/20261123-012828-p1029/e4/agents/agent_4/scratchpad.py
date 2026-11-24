from pathlib import Path
code = '''from fractions import Fraction
from collections import Counter

def check_telescoping(n):
    assert isinstance(n, int) and n > 0
    coeff = Counter()
    for k in range(n):
        coeff[k + 1] += 1
        coeff[k] -= 1
    expected = {0: -1, n: 1}
    assert {k:v for k,v in coeff.items() if v} == expected

def trace_obstruction(eta):
    eta = Fraction(eta)
    assert eta > 0
    n = eta.denominator // eta.numerator + 1
    check_telescoping(n)
    assert n * eta > 1
    return n, n * eta

if __name__ == '__main__':
    for n in range(1, 1001):
        check_telescoping(n)
    for eta in ['1/3', '1/100', '3/7', '2']:
        n, total = trace_obstruction(eta)
        print(f'eta={eta}: N={n}, N*eta={total}>1')
'''
Path('workspace/agent4_trace_check.py').write_text(code)
exec(compile(code, 'workspace/agent4_trace_check.py', 'exec'))