from pathlib import Path
for name in ['agent1_high_dim_analytic_bridge.md','agent3_local_pohozaev_bridge.md','agent4_green_mass_reduction.md']:
 print('\n\n===== '+name+' =====\n')
 print(Path('experiments/e3',name).read_text())
