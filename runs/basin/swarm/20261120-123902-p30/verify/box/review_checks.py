from pathlib import Path
import runpy

print('Rerunning final scratchpad')
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')

print('Rerunning exact code as printed in final reply')
text = Path('record/finals.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'final_code', 'exec'), {})
