from pathlib import Path
import time
root=Path('/mnt')
# Sandbox tools expose the team's files through relative workspace paths.
for name in ['lower_bound_checks.py','slow_hamiltonian_checks.py','agent2_local_germ_checks.py','agent3_arc_checks.py']:
    path=Path('workspace')/name
    source=path.read_text()
    # Agent 2's final line writes back its own source; suppress only that write.
    source='\n'.join(line for line in source.splitlines() if not line.startswith("Path('workspace/agent2_local_germ_checks.py').write_text"))
    print('RUN', name, flush=True)
    exec(compile(source,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})
print('Four decisive shared check files passed.')
# Execute the exact consolidated code in the final answer as well.
text=Path('record/finals.md').read_text()
code=text.split('```python\n',1)[1].split('```',1)[0]
print('RUN consolidated final-answer code',flush=True)
exec(compile(code,'final_answer_checks','exec'),{'__name__':'__main__'})
