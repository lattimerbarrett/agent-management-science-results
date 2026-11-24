from pathlib import Path
import runpy
print('Rerunning saved scratchpad:')
runpy.run_path('agents/agent_1/scratchpad.py')
print('Rerunning exact code from final answer:')
s = Path('record/finals.md').read_text()
code = s.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code, 'final_answer_code', 'exec'), {})
# Independently derive coefficients as suffix sums of signed degree sums.
for m in range(4,101):
    for n, signs in [(2*m,[-1]*m+[1]*m), (2*m+1,[-1]*m+[1]*(m+1))]:
        coeff = [sum(signs[i:]) for i in range(1,n)]
        expected = ([min(i,n-i) for i in range(1,n)] if n%2==0
                    else [i+1 if i<=m else n-i for i in range(1,n)])
        assert coeff == expected
        minval = sum(coeff)-sum(sorted(coeff,reverse=True)[:7])
        assert minval == (m*m-7*m+12 if n%2==0 else m*m-5*m+5)
        if n%2==0:
            zeros = sorted(range(1,n), key=lambda i:coeff[i-1], reverse=True)[:7]
            assert set(zeros)==set(range(m-3,m+4))
            d=[0]
            for j in range(1,n): d.append(d[-1]+(j not in zeros))
            assert d[m-1]==m-4
        else:
            assert minval%2==1
for a in range(1000):
    assert a*(a-1)//2>=6*a-21
    assert (a*(a-1)//2==6*a-21)==(a in (6,7))
print('Independent signed-sum and equality-case checks passed.')
