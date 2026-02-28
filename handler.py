import os
import json

import zasm
import azstd.file.json as ajson

class BaseAI:
	def __init__(self, ai_core, setup):
		conf = ajson.gracefulLoadJSON('config.json')
		self.ai = ai_core(context_len=15, id_='Manager', model='qwen2.5:7b')
		self.ai.set_api(conf['api'])
		self.setup = setup

	def jmsg(self, id, recv, flag, msg):
		return {'id': id, 'recv': recv, 'flag': flag, 'msg': msg}
	
	def online(self):
		self.ai.query(self.setup + '\n---\n' + self.setup, role='system')

	def flush_context(self):
		self.ai.flush_context()

	def dumps_context(self):
		return self.ai.dumps_context()

	def query(self, q):
		return self.ai.query(q)


class AIMgr:
	def __init__(self, ai_core, setup):
		self.ai = BaseAI(ai_core, setup)
		self.isOnline = False

	def query(self, q):
		## q = {id, recv, flag, msg}
		if self.isOnline == False:
			self.ai.online()
			self.isOnline = True
		if q['id'] == 'user':
			if q['msg'] == '/flush':
				self.ai.flush_context()
				return self.ai.jmsg('mgr', 'user', 'chat', 'Memory flushed!')
			elif q['msg'] == '/dump':
				return self.ai.jmsg('mgr', 'user', 'chat', str(self.ai.dumps_context()))

			resp = self.ai.query(q['msg'])
			if resp[:4] != '000+':
				return self.ai.jmsg('mgr', 'user', 'chat', resp)
			else:
				usr_req = resp[4:]
				return self.ai.jmsg('mgr', 'worker', 'request', usr_req)


class AIWorker:
	def __init__(self, ai_core, setup):
		self.ai = BaseAI(ai_core, setup)
		self.isOnline = False
		self.zasm = zasm.Interpreter()

	def query(self, q):
		## q = {id, recv, flag, msg}
		if self.isOnline == False:
			self.ai.online()
			self.isOnline = True

		q_msg = q['msg']
		resp = self.ai.query(q_msg)
		if resp[:5] == '9999 ':
			return self.ai.jmsg('worker', 'user', 'info', resp)
		else:
			print(resp)
			return self.ai.jmsg('worker', 'user', 'exec', resp)