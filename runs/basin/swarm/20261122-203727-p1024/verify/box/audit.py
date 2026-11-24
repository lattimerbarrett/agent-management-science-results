import runpy, sys, time
from pathlib import Path
print('Rerunning archived scratchpad:')
start=time.time()
runpy.run_path('agents/agent_1/scratchpad.py',run_name='__main__')
print('elapsed',time.time()-start)
# The final reply includes a mildly rewritten copy of the code. Run it too.
text=Path('record/finals.md').read_text()
code=text.split('```python\n',1)[1].split('\n```',1)[0]
print('\nRerunning code as printed in final reply:')
ns={'__name__':'__main__'}
exec(compile(code,'final_reply.py','exec'),ns)
# Check pole exponents from the formulas independently of coefficients over many genera.
# a=2g-1 bounds the pole of phi. Derivative term has pole a+1.
for g in range(2,501):
    r,k,N,D,M,K,P=ns['constants'](g)
    a=2*g-1
    for n in range(N):
        for ell in range((N-1-n)//k+1):
            # Upper bounds for pole orders of the six sorts of entries.
            bounds=[n+ell*a, n+ell*a+1, n+ell*a-(a-1),
                    ell*(a-k)-n, ell*(a-k)-n+a-1,
                    ell*(a-k)-n+a]
            if n+(ell+1)*k<N:
                bounds += [n+ell*a+a+1, ell*(a-k)-n+2*a-k]
            assert max(bounds)<=D,(g,n,ell,D,bounds)
print('Uniform pole exponent inequalities passed for g=2,...,500')
