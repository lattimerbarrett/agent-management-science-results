from pathlib import Path
p=Path('workspace/agent2_original_sat.py').read_text()
p=p.replace("print('vars',len(B),'initial constraints',len(sol.assertions()),flush=True)","""print('vars',len(B),'initial constraints',len(sol.assertions()),flush=True)
# Since k=t, every selected F and every v in F require a singleton-intersection witness.
for a,F in enumerate(edges):
 for v in F:
  wit=[B[b] for b,G in enumerate(edges) if F&G=={v}]
  sol.add(z3.Implies(B[a],z3.Or(wit)))
print('singleton constraints added',len(sol.assertions()),flush=True)""")
p=p.replace("Path('workspace/agent2_original_sat.py').write_text", "Path('workspace/agent2_original_critical_sat.py').write_text")
p=p.replace("sol.set(timeout=90000)","sol.set(timeout=60000)")
exec(compile(p,'<critical-sat>','exec'))
