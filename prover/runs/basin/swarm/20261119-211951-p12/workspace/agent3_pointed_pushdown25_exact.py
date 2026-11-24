from pathlib import Path
source=Path('workspace/agent3_pointed_pushdown25.py').read_text().split("old=json.load")[0]
source=source.replace('rows.append([mod(x) if x else 0 for x in row])','rows.append(row)')
exec(source)
from sage.all import QQ
old=json.load(open('workspace/agent3_fz25.json'));oldrows=[[QQ(x) for x in row] for row in old['rows']]
print('exactQQcombinedrank',matrix(QQ,oldrows+rows).rank(),flush=True)
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_pointed_pushdown25_exact.py').write_text(Path(__file__).read_text())
