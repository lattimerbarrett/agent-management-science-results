from pathlib import Path
import runpy
print('=== original scratchpad ===')
runpy.run_path('agents/agent_1/scratchpad.py')
print('=== final displayed code ===')
s = Path('record/finals.md').read_text()
code = s.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code, 'final_displayed_code.py', 'exec'), {})
