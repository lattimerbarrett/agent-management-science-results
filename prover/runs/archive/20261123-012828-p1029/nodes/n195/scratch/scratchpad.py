import os
for root,dirs,files in os.walk('experiments'):
 print(root, files)
 if root.count(os.sep)>1: dirs[:]=[]
