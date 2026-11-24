from pathlib import Path
src=Path('agents/agent_1/scratchpad.py').read_text()
src=src.replace(" save(hr,'hr%s'%r); save(Gs[r],'gr%s'%r)"," assert hr == load('agents/agent_1/hr%s.sobj'%r); assert Gs[r] == load('agents/agent_1/gr%s.sobj'%r)")
exec(compile(src,'rerun_team','exec'))
