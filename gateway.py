import json
import asyncio
import websockets

import handler
import ailib.ollama as ollama

class Gateway:
	def __init__(self, host="localhost", port=9000):
		self.host = host
		self.port = port
		self._server = None
		self.client_conn = {
			"user": None,
			"mgr": None,
			"worker": None
		}
		# self.ai_group = handler.AIRoom(ollama.AI)

	# ====== Lifecycle hooks (leave empty as requested) ======
	async def on_server_start(self):
		pass

	async def on_server_stop(self):
		pass

	async def on_client_connect(self, ws):
		pass

	async def on_client_disconnect(self, ws):
		pass

	async def on_message_received(self, ws, message: str):
		print(message)

	# ====== Core handler ======
	async def handler(self, ws):
		await self.on_client_connect(ws)
		try:
			async for message in ws:
				await self.on_message_received(ws, message)
				jmsg = json.loads(message)

				if jmsg['flag'] == 'hello':
					self.client_conn[jmsg['id']] = ws

				elif jmsg['flag'] == 'chat':
					if jmsg['recv'] == 'user':
						message = jmsg['msg']
						await self.client_conn[jmsg['recv']].send(message)
					else:
						if self.client_conn[jmsg['recv']] == None:
							await self.client_conn['user'].send(f"** [{jmsg['recv']}] is not online...")
						else:
							await self.client_conn[jmsg['recv']].send(message)
							## CC to user
							if jmsg['id'] != 'user':
								await self.client_conn['user'].send(message)

		except websockets.ConnectionClosed:
			pass
		finally:
			await self.on_client_disconnect(ws)

	# ====== Start/Stop ======
	async def start(self):
		await self.on_server_start()
		self._server = await websockets.serve(self.handler, self.host, self.port)
		print(f"WebSocket server listening on ws://{self.host}:{self.port}")
		return self._server

	async def run_forever(self):
		await self.start()
		try:
			await asyncio.Future()  # run forever
		finally:
			await self.stop()

	async def stop(self):
		if self._server is not None:
			self._server.close()
			await self._server.wait_closed()
			self._server = None
		await self.on_server_stop()


async def main():
	server = Gateway("localhost", 9000)
	await server.run_forever()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass