from pathlib import Path
p = Path('record/finals.md').read_text()
code = p.split('```python\n',1)[1].split('\n```',1)[0]
exec(compile(code, 'final_proof_checks.py', 'exec'), {'__name__':'__main__'})
