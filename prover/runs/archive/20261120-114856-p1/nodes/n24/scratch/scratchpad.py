import os
print(os.getcwd())
print(os.listdir('.'))
print(os.listdir('experiments'))
for root,dirs,files in os.walk('/mnt'):
    if 'experiments' in root: print(root,files[:10])
