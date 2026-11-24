from pathlib import Path
Path('workspace/agent1_finite_template_search.py').write_text(Path('scratchpad.py').read_text())
import mpmath as mp
print(2*mp.besseli(1,2*mp.sqrt(2))/(mp.sqrt(2)*mp.besseli(0,2*mp.sqrt(2))))
