from pathlib import Path
for filename in ['adapted_ball_agent2.py','agent1_fusion_checks.py','cone_agent4.py','lower_cuplength_agent3.py']:
    print('\nRunning', filename, flush=True)
    text = Path('/mnt/placeholder').as_posix() if False else Path('workspace', filename).read_text()
    text = '\n'.join(line for line in text.splitlines() if not line.startswith("Path('workspace/"))
    exec(compile(text, filename, 'exec'), {'__name__':'__main__'})
