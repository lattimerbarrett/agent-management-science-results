from pathlib import Path
p=Path('experiments/e1/agent4_exact_full_hessian.py')
s=p.read_text()
s='\n'.join(line for line in s.splitlines() if not (line.startswith('Path(') and '.write_text(' in line))
exec(compile(s,str(p),'exec'), {'__name__':'__main__','__file__':str(p)})
