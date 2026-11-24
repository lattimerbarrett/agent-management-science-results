"""Where things live in this repo."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BENCHMARKS = DATA / "benchmarks"          # sources/, problems/, splits.json (written by `lab data`)
CACHE = DATA / "cache"                    # model replies, and what agents' Python did
EXPERIMENTS = ROOT / "experiments"
MODELS = ROOT / "models"                  # fine-tuned models, each a folder mlx-lm can load
