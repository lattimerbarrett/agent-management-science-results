from pathlib import Path
p=Path('experiments/e3/boundary_yamabe_verified/workspace')
for f in p.glob('*.py'):
 for i,line in enumerate(f.read_text().splitlines(),1):
  if any(k in line for k in ['write_text','write_bytes',"'w'",'"w"','save(','savez(','makedirs','mkdir','unlink(']):print(f.name,i,line)
