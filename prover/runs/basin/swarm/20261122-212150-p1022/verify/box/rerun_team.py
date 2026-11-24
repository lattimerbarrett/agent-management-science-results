from pathlib import Path
p = Path('agents/agent_1/scratchpad.py')
exec(compile(p.read_text(), str(p), 'exec'))
