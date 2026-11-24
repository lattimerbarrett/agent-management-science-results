import os
for base in ['experiments/e1','experiments/e2']:
    print('\nDIRECTORY',base)
    if os.path.isdir(base):
        for root,dirs,files in os.walk(base):
            for name in files:
                if name.endswith(('.md','.txt','.tex','.py','.json')):
                    p=os.path.join(root,name)
                    print(p)
    else: print('Not present')
