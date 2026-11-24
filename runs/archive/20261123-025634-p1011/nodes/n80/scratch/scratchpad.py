from pathlib import Path
for name in ['experiments/e1/agent2_geometry.md','experiments/e3/agent4_green_mass_reduction.md','experiments/e1/agent2_green_correction_check.py']:
 p=Path(name)
 print('\nFILE',name,'\n',p.read_text()[:16000] if p.exists() else 'missing')
