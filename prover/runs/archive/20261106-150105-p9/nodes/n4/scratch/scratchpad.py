import os
print('cwd:',os.getcwd())
print('files:',os.listdir('.'))
for path in ['.home','..']:
    try:
        print(path, os.listdir(path)[:60])
    except OSError as e:
        print(type(e).__name__, str(e))
