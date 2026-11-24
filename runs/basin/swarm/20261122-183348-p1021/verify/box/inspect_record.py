import json
x=json.load(open('agents/agent_1/conversation.json'))
for i,z in enumerate(x['messages']):
 print(i,z.keys())
 if i<4:print(str(z)[:3000])
