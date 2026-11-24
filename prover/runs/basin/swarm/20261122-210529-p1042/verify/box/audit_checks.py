from pathlib import Path
import sympy as s
from itertools import product
from math import factorial, comb
# Recheck the displayed Euler polynomial symbolically over QQ.
m=s.symbols('m')
expr=0
for a,b,c in product(range(3), repeat=3):
    k=a+b+c
    if k<=4:
        expr += ((-1)**k * s.prod(m-i for i in range(k))
                 * s.prod(m-k-1-i for i in range(4-k))
                 / (factorial(a)*factorial(b)*factorial(c)*factorial(4-k)))
poly=(m**4+14*m**3-m**2+34*m+24)/24
assert s.expand(expr-poly)==0
for n in range(7,41):
    ec=0
    for sizes in product(range(3),range(3),range(3),range(n-4)):
        k=sum(sizes)
        if k<=n:
            ec += (-1)**(k+1) * factorial(n)//(factorial(n-k)*factorial(sizes[0])*factorial(sizes[1])*factorial(sizes[2])*factorial(sizes[3]))
    assert ec==(-1)**(n-2)*poly.subs(m,n)
print('Euler polynomial verified symbolically and directly for 7<=m<=40', flush=True)
# Execute the exact final-answer code, not just the scratchpad version.
text=Path('record/finals.md').read_text()
code=text.split('```python\n')[1].split('```')[0]
exec(compile(code,'final_answer_code.py','exec'))
