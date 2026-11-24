import os
for root, dirs, files in os.walk('experiments'):
 if root.count(os.sep)>2:
  dirs[:]=[];continue
 print(root, len(files))
 print('\n'.join(f for f in files if ('summary' in f or 'reduction' in f or 'central' in f or 'spectrum' in f or 'README' in f)))