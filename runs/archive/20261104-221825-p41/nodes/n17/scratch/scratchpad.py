import os
for id in ['e2','e3']:
 print('\n',id)
 for f in os.listdir('experiments/'+id):
  if f.endswith('.md') or 'upper' in f or 'universal' in f: print(f)
print(open('experiments/e2/agent2_lower_universal_result.json').read()[:5000])
print(open('experiments/e2/agent2_lower_universal.py').read()[:12000])