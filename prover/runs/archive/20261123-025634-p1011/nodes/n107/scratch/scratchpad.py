from pathlib import Path
for name in ['agent2_second_radius_reduction.md','agent2_conditional_simple_estimate.md']:
 print('\n===='+name+'====\n'+(Path('experiments/e3')/name).read_text())
