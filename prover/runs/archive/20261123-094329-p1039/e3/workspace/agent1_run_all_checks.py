from pathlib import Path
files = ['agent2_necessity_checks.py', 'agent2_local_graph_checks.py', 'agent2_qcomplete_checks.py', 'agent3_convex_sections_checks.py', 'agent4_levi_checks.py']
for f in files:
    p=Path("workspace")/f
    exec(compile(p.read_text(),str(p),"exec"),{"__name__":"__main__"})
print("All five exact verifiers passed.")
