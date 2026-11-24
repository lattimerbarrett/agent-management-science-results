import os
for root,dirs,files in os.walk('experiments'):
 if root.count(os.sep)<3:
  print(root,files[:30])
