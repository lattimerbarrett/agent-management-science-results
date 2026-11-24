from pathlib import Path
code=Path('record/finals.md').read_text().split('```python\n',1)[1].split('```',1)[0]
exec(compile(code,'final_certificate.py','exec'))
