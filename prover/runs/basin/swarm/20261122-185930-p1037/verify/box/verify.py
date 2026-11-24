from pathlib import Path
import time
s = Path('record/finals.md').read_text().split('```python\n',1)[1].split('```',1)[0]
start=time.monotonic()
exec(compile(s,'final_certificate.py','exec'))
print('Independent rerun elapsed',time.monotonic()-start)
