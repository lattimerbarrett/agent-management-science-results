from pathlib import Path
import re
text=Path('record/finals.md').read_text()
code=re.search(r'```python\n(.*?)\n```',text,re.S).group(1)
exec(compile(code,'final_code','exec'),{})
