from pathlib import Path
# Rerun the team's saved checks and the exact final-response code.
p=Path('agents/agent_1/scratchpad.py')
exec(compile(p.read_text(),str(p),'exec'))
f=Path('record/finals.md').read_text()
code=f.split('```python\n')[1].split('```')[0]
exec(compile(code,'final_code','exec'))
