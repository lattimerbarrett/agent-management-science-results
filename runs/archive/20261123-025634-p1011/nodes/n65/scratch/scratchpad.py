from pathlib import Path
base=Path('experiments/e6')
p=base/'agent2_unbounded_energy_almost_solutions.md'
print(p.read_text() if p.exists() else '\n'.join(str(x) for x in base.glob('*almost*')))
