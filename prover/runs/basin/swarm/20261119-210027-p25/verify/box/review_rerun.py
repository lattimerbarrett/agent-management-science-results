from pathlib import Path
# Run the consolidated final-answer checks, omitting only its self-copy command.
source = Path('workspace/agent1_answer_code.py').read_text()
source = source.split('from pathlib import Path')[0]
exec(compile(source, 'workspace/agent1_answer_code.py', 'exec'))
print('FINAL-ANSWER CHECKS PASSED')
# Independently exported lower-bound instance, omitting only its JSON write.
source = Path('workspace/agent4_lift_standalone.py').read_text()
source = source.split("with open('workspace/")[0]
exec(compile(source, 'workspace/agent4_lift_standalone.py', 'exec'))
print('INDEPENDENT LOWER INSTANCE PASSED')
