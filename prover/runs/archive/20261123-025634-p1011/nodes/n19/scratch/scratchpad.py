import sys
from pathlib import Path
sys.path.insert(0,str(Path('experiments/e3').resolve()))
from agent2_finite_maxima_certificates import certificate
certificate(19)
