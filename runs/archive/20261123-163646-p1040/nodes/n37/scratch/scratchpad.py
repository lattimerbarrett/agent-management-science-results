from pathlib import Path
for name in ['agent3_stable_symbolic_checks.py','agent4_column_word_checks.py','agent3_odd_hilbert_norm_checks.py']:
 p=Path('experiments/e2')/name
 src='\n'.join(line for line in p.read_text().splitlines() if not line.startswith('Path('))
 print('\nRUN',name,flush=True)
 exec(compile(src,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
