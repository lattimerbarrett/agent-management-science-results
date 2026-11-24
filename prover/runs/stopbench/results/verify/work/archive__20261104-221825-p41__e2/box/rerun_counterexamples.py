from pathlib import Path
for filename in ['workspace/agent1_selfcontained_counterexample.py', 'workspace/agent2_selfcontained_counterexample.py']:
    print('RUN', filename, flush=True)
    exec(compile(Path(filename).read_text(), filename, 'exec'), {'__name__':'__main__', '__file__':filename})
