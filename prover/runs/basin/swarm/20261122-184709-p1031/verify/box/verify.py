from pathlib import Path
text = Path('record/finals.md').read_text()
code = text.split('```python\n', 1)[1].split('```', 1)[0]
exec(compile(code, 'final_answer_code', 'exec'))

# Additional exact checks of the identities and global estimates used in the proof.
from fractions import Fraction
from math import comb
for n in range(2,81):
    for r in range(1,n):
        F1=sum((-1)**(r-j)*comb(n,j) for j in range(r))+sum(comb(n,j) for j in range(r,n+1))
        assert F1==2*sum(comb(n-1,i) for i in range(n-r))
        A=2*sum(comb(n-1,i) for i in range(r))
        if 2*r<=n:
            assert n*3**r <= 2*r*2**n
        else:
            assert A >= 2**(n-1)
        if n>=3:
            assert Fraction(comb(n,r)*3**r,4**n)<=Fraction(27,64)
for q in range(3,101):
    assert 3*(2**q-2)>=2*q*q
print('Additional exact checks of the proof identities and bounds passed.')
