p='workspace/agent4_fz_check.py'
s=open(p).read();s=s.replace("with open('workspace/agent4_fz_check.py','w') as f:f.write(open('scratchpad.py').read())\n",'')
open(p,'w').write(s)
print('Removed self-overwrite line from independent upper script.')
