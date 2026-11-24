from pathlib import Path
import runpy
runpy.run_path('agents/agent_1/scratchpad.py', run_name='__main__')
# Also execute the final answer's actual code, not only the saved scratchpad.
text = Path('record/finals.md').read_text()
code = text.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code, 'final_answer_code', 'exec'), {})
