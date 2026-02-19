# -*- coding: utf-8 -*-
import json
import time
import azstd.api as aapi

class AI:
	def __init__(self, context_len=999, id_='MyAI', model=None, stream=False):
		self.apiMgr = None
		self.context = []
		self.context_len = context_len
		self.id_ = id_
		self.__console(f'Powered by Ollama. Context length: {context_len}')
		self.model = model
		self.stream = stream
	
	def set_api(self, host, key=None):
		self.apiMgr = aapi.API(host)
		# self.apiMgr.add_header('api-key', key)

	def __console(self, msg, level=1):
		d_lv = {0: 'DEBUG', 1: 'INFO', 2: 'WARN', 3: 'ERROR'}
		print(f"[AI: {self.id_}][{d_lv[level]}] {msg}")
	
	def __parse_resp(self, resp):
		j_resp = json.loads(resp['text'])
		return j_resp['message']['content']

	def __create_query(self, content, role='user'):
		o_msg = {'role': role, 'content': content}
		if role == 'system':
			self.context = []
		self.context.append(o_msg)
		if len(self.context) > self.context_len:
			self.__trim_context()
		return {'model': self.model, 'stream': self.stream, 'messages': self.context}

	def __trim_context(self):
		n_morethan = len(self.context) - self.context_len
		for i in range(n_morethan):
			if self.context[0]['role'] == 'system':
				del self.context[1]
			else:
				del self.context[0]
			self.__console('Context trimed.')
		return 0

	def dumps_context(self):
		return self.context
	
	def dumps_context_string(self):
		dia = []
		for qo in self.context:
			dia.append('%s: %s' % (qo['role'], qo['content']))
		return dia
	
	def loads_context(self, context):
		self.context = context
	
	def flush_context(self, isProtectSystem=True):
		if isProtectSystem == True and self.context[0]['role'] == 'system':
			self.context = self.context[1:]
		else:
			self.context = []
		self.__console('Context flushed.')
	
	def query(self, q, role='user'):
		self.apiMgr.set_body(self.__create_query(q, role))
		resp = self.apiMgr.post()
		self.__console(f'Message sent. Context length: {len(self.context)}/{self.context_len}')
		try:
			resp_text = self.__parse_resp(resp)
			self.context.append({'role': role, 'content': resp_text})
		except:
			resp_text = '** ERR: Unexpected response, retry please.\n-----\n%s' % resp
		return resp_text

