# Inspect the previously saved random-search code without executing it.
# Current file has instead been the cycle SAT search; inspect experiment notes.
import os
for team in ['e2','e4']:
 print('\nTEAM',team)
 for root,dirs,files in os.walk('experiments/'+team):
  for f in files:
   if f.endswith(('.txt','.md','.json')):
    p=os.path.join(root,f)
    print(p)
