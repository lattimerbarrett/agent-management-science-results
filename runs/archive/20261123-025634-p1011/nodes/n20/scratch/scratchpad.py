from pathlib import Path
for f in ['experiments/e1/agent2_geometry.md','experiments/e1/agent2_single_patch_audit.md','experiments/e1/agent1_single_patch_audit.md']:
 print('\n###',f,'\n',Path(f).read_text()[:24000])
