from pathlib import Path
for name in ['agent1_extremal_reduction.md','agent4_reduction_notes.md','agent2_product_checks.py']:
 p=Path('experiments/e1')/name
 print('\n###',name,'\n',p.read_text()[:20000])
