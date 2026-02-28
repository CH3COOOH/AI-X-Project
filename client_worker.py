import json
import asyncio
import websockets
import re

import handler
import ailib.ollama as ollama
import azstd.file.rw as rw

class WorkerClient:
	def __init__(self, uri="ws://localhost:9000"):
		self.uri = uri
		self.id = 'worker'
		zasmdoc = rw.read_t8('skills/zasm.md')
		skill_worker = rw.read_t8('skills/worker.md').replace('{{ zasm_doc }}', zasmdoc)
		self.ai = handler.AIWorker(ollama.AI, skill_worker)

	def __form_msg(self, recv, flag, msg):
		return {
			'id': self.id,
			'recv': recv,
			'flag': flag,
			'msg': msg
		}

	async def on_message_received(self, msg, ws):
		print(msg)
		resp = self.ai.query(json.loads(msg))
		await ws.send(json.dumps(resp, ensure_ascii=False))

	async def start(self):
		async with websockets.connect(self.uri) as ws:
			await ws.send(json.dumps(self.__form_msg('center', 'hello', 'WORKER Online.')))
			while True:
				msg = await ws.recv()
				await self.on_message_received(msg, ws)


if __name__ == "__main__":
	try:
		client = WorkerClient()
		asyncio.run(client.start())
	except KeyboardInterrupt:
		pass