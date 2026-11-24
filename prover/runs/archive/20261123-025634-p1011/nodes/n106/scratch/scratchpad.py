from pathlib import Path
b=Path('experiments/e3')
for f in ['agent2_second_radius_reduction.md','agent2_selection_lemma.md','agent2_conditional_simple_estimate.md','agent2_cluster_reduction.md']:
 t=(b/f).read_text();print('\nFILE',f,'\n',t[:18000])
t=(b/'agent3_local_pohozaev_bridge.md').read_text();a=t.index('## Step 3');b1=t.index('## Step 5');print('\nLOCAL STEPS 3/4\n',t[a:b1])
