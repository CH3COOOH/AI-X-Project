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

	def jmsg(self, recv, flag, msg):
		return {'id': 'mgr', 'recv': recv, 'flag': flag, 'msg': msg}
	
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
		if self.isOnline == False:
			self.ai.online()
			self.isOnline = True	
		if q == '/flush':
			self.ai.flush_context()
			return self.ai.jmsg('user', 'chat', 'Memory flushed!')
		elif q == '/dump':
			return self.ai.jmsg('user', 'chat', str(self.ai.dumps_context()))

		resp = self.ai.query(q)
		if resp[:4] != '000+':
			return self.ai.jmsg('user', 'chat', resp)
		elif resp[:4] == '000+':
			usr_req = resp[4:]
			return self.ai.jmsg('worker', 'reqest', usr_req)


class AIWorker:
	def __init__(self, ai_core, setup):
		self.ai = BaseAI(ai_core, setup)
		self.isOnline = False
		self.zasm = zasm.Interpreter()

	def query(self, q):
		if self.isOnline == False:
			self.ai.online()
			self.isOnline = True

		resp = self.ai.query(q)
		if resp[:5] == '9999 ':
			return self.ai.jmsg('mgr', 'info', resp)
		else:
			print(resp)
			