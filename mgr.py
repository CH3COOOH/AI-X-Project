import json
import asyncio
import websockets

import handler
import ailib.ollama as ollama

class ChatClient:
	def __init__(self, uri="ws://localhost:9000"):
		self.uri = uri
		self.ai = handler.AIMgr(ollama.AI, 'skills/mgr.md')

	def __form_msg(self, recv, flag, msg):
		return {'id': 'mgr', 'recv': recv, 'flag': flag, 'msg': msg}

	async def on_message_received(self, msg, ws):
		print(msg)
		jmsg = json.loads(msg)
		if jmsg['flag'] == 'chat':
			resp = self.ai.query(jmsg['msg'])
			await ws.send(json.dumps(resp, ensure_ascii=False))

	async def start(self):
		async with websockets.connect(self.uri) as ws:
			await ws.send(json.dumps(self.__form_msg('center', 'hello', 'MGR Online.')))
			while True:
				msg = await ws.recv()
				await self.on_message_received(msg, ws)


if __name__ == "__main__":
	try:
		client = ChatClient()
		asyncio.run(client.start())
	except KeyboardInterrupt:
		pass