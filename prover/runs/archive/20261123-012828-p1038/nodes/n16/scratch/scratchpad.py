from pathlib import Path
p=Path('experiments/e1')
for name in ['agent4_pick_rank_obstruction.md','agent2_blocks.py']:
 print('\n===== '+name+' =====\n')
 print((p/name).read_text()[:24000])
