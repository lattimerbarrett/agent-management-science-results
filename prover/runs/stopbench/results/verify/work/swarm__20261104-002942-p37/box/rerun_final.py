from pathlib import Path
import sys
sys.path.insert(0, 'workspace')
s=Path('record/finals.md').read_text()
code=s.split('```python',1)[1].split('```',1)[0]
exec(compile(code, 'final_embedded_checker.py', 'exec'), {'__name__':'__main__'})
