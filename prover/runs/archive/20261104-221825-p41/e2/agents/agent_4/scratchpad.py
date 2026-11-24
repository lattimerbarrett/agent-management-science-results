from pathlib import Path
source=Path('workspace/agent2_selfcontained_counterexample.py').read_text()
exec(compile(source,'workspace/agent2_selfcontained_counterexample.py','exec'),{'__name__':'independent_verification','__file__':'workspace/agent2_selfcontained_counterexample.py'})
print('Agent4 independently ran unchanged agent2 portable certificate successfully.')