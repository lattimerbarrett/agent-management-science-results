from pathlib import Path
code = Path('agents/agent_1/scratchpad.py').read_text()
exec(compile(code, 'agents/agent_1/scratchpad.py', 'exec'))
assert c == 1 + 4*h + 9*h**2 + 14*h**3 + 14*h**4
print('Final full Chern assertion also passed.')
