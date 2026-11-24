from pathlib import Path
base=Path('experiments/e3')
for f in ['agent2_selection_lemma.md','agent2_conditional_simple_estimate.md','agent2_second_radius_reduction.md','agent2_cluster_reduction.md']:
 p=base/f
 if p.exists():
  t=p.read_text(); print('\n###',f,'\n',t[:19000])
