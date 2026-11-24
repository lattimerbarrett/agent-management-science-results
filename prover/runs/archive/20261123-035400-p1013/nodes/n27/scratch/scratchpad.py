import os
print('cwd',os.getcwd())
print('here',os.listdir('.'))
print('parent',os.listdir('..'))
for p in ['experiments','../experiments','/workspace/experiments']:
    if os.path.exists(p):
        print(p, list(os.walk(p))[:10])
