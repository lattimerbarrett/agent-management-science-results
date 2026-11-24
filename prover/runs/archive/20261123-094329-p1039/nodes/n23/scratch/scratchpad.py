import os
for e in ['e2','e3','e5','e6']:
 d='experiments/'+e
 print('\n',e,os.listdir(d))
for path in ['experiments/e3/agent1_conditional_qcomplete_proof.txt','experiments/e3/agent2_local_polyconvexity.txt','experiments/e5/agent1_verified_partial.txt']:
 if os.path.isfile(path):
  print('\nFILE',path); print(open(path).read()[:16000])
