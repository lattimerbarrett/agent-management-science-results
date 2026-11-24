import ast,contextlib,io
from pathlib import Path
class Safe(ast.NodeTransformer):
 def visit_Expr(self,node):
  if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='write_text':return ast.copy_location(ast.Pass(),node)
  return self.generic_visit(node)
p=Path('workspace/agent4_exact18_blocks.py');t=ast.fix_missing_locations(Safe().visit(ast.parse(p.read_text())))
o=io.StringIO()
with contextlib.redirect_stdout(o):exec(compile(t,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
print(o.getvalue())
