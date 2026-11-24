from pathlib import Path
for name in ['agent2_blocks.py','agent4_m1_search.json','agent2_core_ratio_results.json','agent4_interval_counterexample.json']:
 print('\nFILE',name,'\n',Path('experiments/e1',name).read_text()[:32000])
