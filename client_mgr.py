import json
import asyncio
import websockets

import handler
import ailib.ollama as ollama
import azstd.file.rw as rw

class MgrClient:
	def __init__(self, uri="ws://localhost:9000"):
		self.uri = uri
		self.id = 'mgr'
		self.ai = handler.AIMgr(ollama.AI, rw.read_t8('skills/mgr.md'))

	def __form_msg(self, recv, flag, msg):
		return {
			'id': self.id,
			'recv': recv,
			'flag': flag,
			'msg': msg
		}

	async def on_message_received(self, msg, ws):
		print(msg)
		jmsg = json.loads(msg)
		resp = self.ai.query(json.loads(msg))
		await ws.send(json.dumps(resp, ensure_ascii=False))

	async def start(self):
		async with websockets.connect(self.uri) as ws:
			await ws.send(json.dumps(self.__form_msg('center', 'hello', 'MGR Online.')))
			while True:
				msg = await ws.recv()
				await self.on_message_received(msg, ws)


if __name__ == "__main__":
	try:
		client = MgrClient()
		asyncio.run(client.start())
	except KeyboardInterrupt:
		pass