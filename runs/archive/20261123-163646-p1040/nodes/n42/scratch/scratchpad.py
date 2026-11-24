from pathlib import Path
for name in ['agent3_stable_symbolic_checks.py','agent4_column_word_checks.py']:
 p=Path('experiments/e2')/name
 src=p.read_text();src='\n'.join(line for line in src.splitlines() if '.write_text(' not in line)
 print(name,flush=True)
 exec(compile(src,str(p),'exec'),{'__name__':'__main__'})