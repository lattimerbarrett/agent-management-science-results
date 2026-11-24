from pathlib import Path
for f in ['experiments/e3/agent1_high_dim_analytic_bridge.md','experiments/e3/agent2_finite_profiles.txt']:
 print('\n###',f,'\n',Path(f).read_text()[:50000])
