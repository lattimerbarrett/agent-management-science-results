from pathlib import Path
for f in ['experiments/e3/agent3_general_blocks.py','experiments/e3/agent1_moment_proof.txt','experiments/e3/agent2_n19_critical_certificate.py']:
 print('\n###',f,'\n',Path(f).read_text()[:22000])
