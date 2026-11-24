from pathlib import Path
p=Path('workspace/billiard_words_agent2.py').read_text();print(p[:16000])
import numpy as np
p=np.load('workspace/survivor_best_agent2.npz');print({k:p[k] for k in ['a','L','H','depth']})
