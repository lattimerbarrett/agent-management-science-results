from pathlib import Path
s=Path('workspace/survivor_agent2.py').read_text()
s=s.replace("if I[0]<I[1]:ans.append((M,I))","if I[0]<I[1]:\n    eps=max(1e-16,(I[1]-I[0])*1e-9);I=(I[0]+eps,I[1]-eps)\n    if I[0]<I[1]:ans.append((M,I))")
Path('workspace/survivor_fixed_agent2.py').write_text(s)
exec(compile(s,'survivor-fixed','exec'))
