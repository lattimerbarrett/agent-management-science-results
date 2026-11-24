import os
for root, ds, fs in os.walk('experiments'):
    for f in fs:
        if f.endswith('.md') and ('partial' in f or 'reduction' in f or 'extremal' in f):
            p=os.path.join(root,f)
            print('\nFILE',p)
            text=open(p).read()
            print(text[:20000])
