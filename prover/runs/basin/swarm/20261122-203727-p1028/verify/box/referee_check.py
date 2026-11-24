from pathlib import Path
from math import comb

# Run the exact code printed in the final response, regenerating all n=10
# isomorphism classes (no dependence on the agent's saved graph files).
text = Path('record/finals.md').read_text()
code = text.split('```python\n', 1)[1].split('```', 1)[0]
exec(compile(code, 'team_final.py', 'exec'), {'__name__': '__main__'})

# Separately check the explicit one-based bit-position formula against
# the lexicographic edge ordering used in the verification code.
for n in range(2, 101):
    positions = [((i-1)*(2*n-i))//2+j-i-1
                 for i in range(1,n+1) for j in range(i+1,n+1)]
    assert positions == list(range(comb(n,2)))
for n in range(2, 6):
    for k in range(2**comb(n,2)):
        for i in range(1,n+1):
            for j in range(i+1,n+1):
                p = ((i-1)*(2*n-i))//2+j-i-1
                a = k//(2**p) - 2*(k//(2**(p+1)))
                assert a == (k>>p)&1
print('Explicit bit-position and digit extraction checks passed.')
