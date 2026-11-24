from pathlib import Path
p=Path('record/finals.md').read_text()
code=p.split('```python\n')[1].split('```')[0]
exec(compile(code,'final_code','exec'))
