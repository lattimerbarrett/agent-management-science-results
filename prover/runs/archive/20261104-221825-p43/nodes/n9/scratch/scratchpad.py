import os
for root,dirs,files in os.walk('experiments'):
    for f in files:
        if f.endswith(('.md','.txt','.py')):
            print(os.path.join(root,f))
