import pathlib
for p in pathlib.Path('workspace').glob('agent3*.py'):
 s=p.read_text();lines=s.splitlines(True)
 clean=''.join(line for line in lines if 'write(open(__file__).read())' not in line)
 if clean!=s:p.write_text(clean);print('removed self-save:',p)
print('exact main verify:')
s=open('workspace/agent3_fz25_exact.py').read();exec(compile(s,'exact.py','exec'))