from pathlib import Path
import runpy
s = Path('/workspace/agent1_finalcheck.py')
# Paths provided by sandbox are relative to review directory.
s = Path('workspace/agent1_finalcheck.py')
text = s.read_text()
text = '\n'.join(line for line in text.splitlines() if "with open('workspace/agent1_finalcheck.py'" not in line)
exec(compile(text, str(s), 'exec'), {'__name__':'__main__'})
runpy.run_path('workspace/agent2_certificate.py',run_name='__main__')
