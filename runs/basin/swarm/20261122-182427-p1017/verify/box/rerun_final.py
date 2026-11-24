from pathlib import Path
s = Path('record/finals.md').read_text()
code = s.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code,'final_proof.py','exec'))
