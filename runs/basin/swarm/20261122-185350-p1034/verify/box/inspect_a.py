from pathlib import Path
src=Path('agents/agent_1/scratchpad.py').read_text().split('Gs={}')[0]
exec(src)
for r in [1,2]:
 print('a',r)
 for k in range(r+1):print([a(r,k,m).factor() for m in range(r+1)])
