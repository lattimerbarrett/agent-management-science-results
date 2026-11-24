from pathlib import Path
b=Path('experiments/e3')
for f,lo,hi in [('agent2_second_radius_reduction.md',1,30),('agent2_conditional_simple_estimate.md',1,25),('agent3_local_pohozaev_bridge.md',40,65),('agent3_local_pohozaev_bridge.md',165,205)]:
 lines=(b/f).read_text().splitlines()
 print('\n###',f)
 for j in range(lo-1,min(hi,len(lines))): print(str(j+1)+': '+lines[j])
