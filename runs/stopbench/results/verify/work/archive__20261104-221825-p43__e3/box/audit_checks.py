from pathlib import Path
p=Path('/workspace/agent1_complete_checks.py')
# sandbox files are addressed relative to the shared root
p=Path('workspace/agent1_complete_checks.py')
src=p.read_text().splitlines()
src='\n'.join(line for line in src if not line.startswith("Path('workspace/agent1_complete_checks.py').write_text"))
exec(compile(src,str(p),'exec'))
print('\n-- interval collapse-axis inequalities --')
p=Path('workspace/agent2_collapse_axes_check.py')
exec(compile(p.read_text(),str(p),'exec'))
