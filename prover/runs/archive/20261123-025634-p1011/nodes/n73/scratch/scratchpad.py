from pathlib import Path
for name in ['experiments/e1/agent2_geometry.md','experiments/e3/agent4_green_mass_reduction.md','experiments/e7/agent3_compactness_bridge.md']:
 p=Path(name)
 print('\n###',name)
 try:
  t=p.read_text();print(t[:6500])
 except Exception as e:print(type(e).__name__,str(e))
