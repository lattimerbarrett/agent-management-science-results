from pathlib import Path
text=Path('../record/finals.md').read_text() if Path('../record/finals.md').exists() else Path('record/finals.md').read_text()
code=text.split('```python\n')[1].split('\n```')[0]
exec(compile(code,'final_code','exec'))
