from pathlib import Path
import ast

# Rerun the team's symbolic checks, skipping only top-level writes into
# its read-only workspace (and the associated output-data persistence).
paths = ['workspace/agent1_complete_checks.py', 'workspace/agent3_numerics.py', 'workspace/agent4_curvature_checks.py']
for path in paths:
    source = Path('/'+path).read_text() if Path('/'+path).exists() else Path('../'+path).read_text() if Path('../'+path).exists() else Path(path).read_text()
    tree = ast.parse(source, filename=path)
    kept=[]
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'write_text':
            continue
        kept.append(node)
    tree.body=kept
    print('RUN',path)
    exec(compile(ast.fix_missing_locations(tree), path, 'exec'), {'__name__':'__main__'})
print('All rerun symbolic assertions passed.')
