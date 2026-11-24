from pathlib import Path
import os,runpy
os.chdir(Path(__file__).resolve().parent)
runpy.run_path('workspace/agent2_all_checks.py',run_name='__main__')
