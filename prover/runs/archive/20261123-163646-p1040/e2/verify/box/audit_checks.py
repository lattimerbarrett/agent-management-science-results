from pathlib import Path
import sys
sys.path.insert(0,'workspace')
# Re-execute the non-writing portions of the team's three relevant scripts.
for path, stop in [('workspace/agent2_derivations.py', "    open('workspace/agent2_degree2_results.json'"), ('workspace/agent3_stable_symbolic_checks.py', "Path('workspace/agent3_stable_symbolic_checks.py')"), ('workspace/agent4_n2_checks.py', 'from pathlib import Path')]:
    print('\nAUDIT', path, flush=True)
    source=Path(path).read_text().split(stop)[0]
    exec(compile(source,path,'exec'), {'__name__':'__main__','__file__':path})
print('All rerun exact assertions passed.')
