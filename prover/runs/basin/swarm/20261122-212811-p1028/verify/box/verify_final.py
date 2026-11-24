from pathlib import Path
text=Path('record/finals.md').read_text()
code=text.split('```python\n',1)[1].split('```',1)[0]
# Execute the exact final verification code, not the cached pickle.
ns={'__name__':'__main__'}
exec(compile(code,'final_submission.py','exec'),ns)
# Check the closed-form bit index against the iterative implementation.
for n in range(2,31):
    inds=[i*(2*n-i-1)//2+j-i-1 for i in range(n) for j in range(i+1,n)]
    assert inds==list(range(n*(n-1)//2))
print('Closed-form bit indexing checked for n=2,...,30')
