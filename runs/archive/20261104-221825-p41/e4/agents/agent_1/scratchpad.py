from pathlib import Path
source=Path('workspace/agent1_saturation_sat.py').read_text()
source=source.replace("s.add(x[fs[0]],z3.Not(z3.And(list(x.values()))))", "s.add(x[fs[0]],z3.Not(z3.And(list(x.values()))))\n s.add(z3.Or([z3.Not(y[g]) for g in y if g.bit_count()==2]))\n for e in [g for g in y if g.bit_count()==2]:\n  u=e&-e;v=e^u\n  for h in [g for g in y if g.bit_count()==m-2 and not g&e]:\n   s.add(z3.Implies(z3.And(y[u|h],y[v|h]),y[e]))")
source=source.replace("  s.add(z3.Or(x[f],blocked))", "  # Full saturation intentionally omitted.")
source=source.replace("open(f'workspace/agent1_stuck_{n}_{m}.json','w')", "open(f'workspace/agent1_graph_incomplete_edge_stuck_{n}_{m}.json','w')")
exec(compile(source,'edge_saturation_search','exec'))
for n,m in [(7,4),(8,4),(9,4)]:find_stuck(n,m,timeout=60000,normal=True)
