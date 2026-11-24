from pathlib import Path
for f in ['agent4_pick_rank_obstruction.md','agent4_fullmode_schur.md','agent4_schur_pick_lemma.md','agent2_blocks.py']:
 print('\n###',f,'\n',Path('experiments/e1',f).read_text())
