from pathlib import Path
src=Path('workspace/verification_standalone.py').read_text().replace('"workspace"','"audit_outputs"').replace("'workspace/", "'audit_outputs/")
exec(compile(src,'standalone-audited','exec'), {'__name__':'__main__'})
