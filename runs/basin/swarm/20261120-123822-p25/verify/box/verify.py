from pathlib import Path
import runpy
print('=== Final-answer code ===')
s = Path('record/finals.md').read_text()
code = s.split('```python\n',1)[1].split('\n```',1)[0]
exec(compile(code, 'finals_code', 'exec'), {})
print('=== Saved scratchpad ===')
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
