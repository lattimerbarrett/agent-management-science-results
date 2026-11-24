from pathlib import Path
print(Path('workspace/exterior_appendix.py').read_text())
exec(compile(Path('workspace/exterior_appendix.py').read_text(),'workspace/exterior_appendix.py','exec'))