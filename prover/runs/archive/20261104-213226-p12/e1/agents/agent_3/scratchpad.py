from pathlib import Path
p=Path('workspace/agent3_lower.py')
s=p.read_text();s=s.split('# copy own complete runnable script')[0]
p.write_text(s)
print('Removed self-copy from reusable lower verifier;',len(s.splitlines()),'lines')
exec(compile(s,str(p),'exec'))
