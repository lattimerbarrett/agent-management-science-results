from pathlib import Path
for name in ['agent2_second_radius_reduction.md','agent2_cluster_reduction.md','agent2_conditional_simple_estimate.md']:
 p=Path('experiments/e3')/name
 print('\n###',name,'###\n',p.read_text())
