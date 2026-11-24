import os
print(os.getcwd())
print(os.listdir('.'))
print(os.listdir('experiments'))
for folder in ['experiments/e2','experiments/e3']:
 print('\n',folder)
 print('\n'.join(os.listdir(folder)))
