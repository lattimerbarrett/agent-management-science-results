from pathlib import Path
for name in ['experiments/e2/agent2_lower_universal.py','experiments/e2/agent2_selfcontained_counterexample.py','experiments/e3/agent4_lower_standalone.py']:
 s=Path(name).read_text();print('\nFILE',name,'len',len(s));print(s[:16000])
