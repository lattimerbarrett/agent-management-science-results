from pathlib import Path
text=Path('/mnt/none') if False else Path('../record/finals.md')
# The sandbox exposes the record and workspace by these relative paths.
for p in [Path('record/finals.md'), Path('../record/finals.md')]:
    if p.exists():
        text=p.read_text(); break
else:
    raise FileNotFoundError('record/finals.md')
code=text.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code,'final_certificate','exec'))
