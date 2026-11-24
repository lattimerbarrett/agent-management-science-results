from pathlib import Path
p=Path('workspace/agent4_cycle_engine.py').read_text()
print(p[:9000])