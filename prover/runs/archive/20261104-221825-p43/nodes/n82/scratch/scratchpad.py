import os
for root,dirs,files in os.walk('experiments'):
    if root.count(os.sep)<2:
        print(root,files)
