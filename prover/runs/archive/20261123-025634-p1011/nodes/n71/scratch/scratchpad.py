import sys
from pathlib import Path
sys.path.insert(0,str(Path('experiments/e3').resolve()))
from agent2_finite_maxima_certificates import certificate
certificate(19)
print('\nUniform certificate source:')
p=Path('experiments/e3/agent4_translation_ge40.py')
print(p.read_text()[:18000])
