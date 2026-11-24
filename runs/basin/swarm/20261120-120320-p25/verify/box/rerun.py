from pathlib import Path
import runpy
p=Path('/tmp/unused')
# The team's script writes no files, so execute it without modification.
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
# Also execute the exact code block printed in the final answer.
s=Path('record/finals.md').read_text()
code=s.split('```python\n',1)[1].split('```',1)[0]
print('\nExecuting final code block:')
exec(compile(code,'final_code','exec'), {'__name__':'__main__'})
