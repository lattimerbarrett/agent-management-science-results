from pathlib import Path
p=Path('record/finals.md').read_text()
script=p.split('```python\n',1)[1].split('\n```',1)[0]
exec(compile(script, 'final_script', 'exec'))
print('Final supplied script: all assertions passed.')
