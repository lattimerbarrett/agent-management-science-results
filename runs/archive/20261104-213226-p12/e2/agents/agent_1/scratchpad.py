from pathlib import Path
p=Path('workspace/agent1_bundle/verify.py').resolve();exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})