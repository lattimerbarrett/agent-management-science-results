import os
for root,ds,fs in os.walk('experiments'):
    if root.count(os.sep)>3:
        ds[:]=[]
    for f in fs:
        if f.endswith(('.md','.txt','.json','.py')):
            print(os.path.join(root,f))
