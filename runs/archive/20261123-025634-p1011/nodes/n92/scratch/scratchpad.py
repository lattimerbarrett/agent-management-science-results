from pathlib import Path
s=Path('experiments/e3/agent3_local_pohozaev_bridge.md').read_text()
print(s[s.index('## Step 5'):])
print('\nE6 UNBOUNDED\n')
p=Path('experiments/e6/agent2_unbounded_energy_almost_solutions.md')
print(p.read_text() if p.exists() else 'missing')
