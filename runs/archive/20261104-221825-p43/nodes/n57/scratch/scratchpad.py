import os
for root, ds, fs in os.walk('experiments'):
 if root.count(os.sep)<3:
  print(root,fs)
