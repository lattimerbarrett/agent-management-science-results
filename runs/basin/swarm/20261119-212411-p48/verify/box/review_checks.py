from pathlib import Path
for who in ['agent_3', 'agent_4']:
    p = Path('/home/oai/share') # not used
    src = Path('../agents/'+who+'/scratchpad.py')
    if not src.exists(): src=Path('agents/'+who+'/scratchpad.py')
    # Tools resolve repo paths separately; locate using absolute sandbox cwd.
    print('Trying source',src)
    code=src.read_text()
    code='\n'.join(line for line in code.splitlines() if not (line.startswith('Path(') and '.write_text(' in line))
    exec(compile(code,str(src),'exec'),{})
