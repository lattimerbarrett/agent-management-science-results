from pathlib import Path
p=Path('experiments/e1/a1_central_all_but_four.py')
s=p.read_text().replace("'workspace/", "'experiments/e1/")
s=s[:s.index("json.dump(summary,")]
exec(compile(s,str(p),'exec'))
p=Path('experiments/e1/agent3_low.py')
ns={'__name__':'__main__'}
exec(compile(p.read_text(),str(p),'exec'),ns)
