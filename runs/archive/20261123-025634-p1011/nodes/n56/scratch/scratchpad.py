from pathlib import Path
for f in ['agent2_second_radius_reduction.md','agent3_local_pohozaev_bridge.md']:
 t=(Path('experiments/e3')/f).read_text()
 if f.startswith('agent3'):
  lines=t.splitlines()
  for i,line in enumerate(lines):
   if any(x in line.lower() for x in ['scale-uniform','second','rescal','simple','radius']):
    print(i+1, '\n'.join(lines[max(0,i-2):min(len(lines),i+5)]))
 else: print(t)
