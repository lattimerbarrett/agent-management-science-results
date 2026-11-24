import os
print('cwd', os.getcwd())
print('entries',os.listdir('.'))
for root,ds,fs in os.walk('experiments'):
    if root.count(os.sep)>3: ds[:]=[]
    for f in fs:
        if 'standalone' in f or 'counterexample' in f or 'universal' in f or 'trap' in f:
            print(os.path.join(root,f))
