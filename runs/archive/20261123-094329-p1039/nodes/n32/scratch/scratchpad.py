from pathlib import Path
files=['experiments/e2/agent2_nonrational_ball_check.py','experiments/e2/agent1_graph_disk_check.py']
for name in files:
 p=Path(name)
 print(name, 'exists:',p.exists())
 if p.exists():
  print(p.read_text()[:14000])
