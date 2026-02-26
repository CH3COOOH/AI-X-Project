import os
import json

import azstd.file.json as ajson
import azstd.file.rw as rw

class BaseAI:
	def __init__(self, ai_core, path_skill):
		conf = ajson.gracefulLoadJSON('config.json')
		self.ai = ai_core(context_len=15, id_='Manager', model='qwen2.5:7b')
		self.ai.set_api(conf['api'])
		self.setup = rw.read_t8(path_skill)

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
	def __init__(self, ai_core, path_skill):
		self.ai = BaseAI(ai_core, path_skill)
		self.ai.online()

	def query(self, q):
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
			return self.ai.jmsg('user', 'chat', usr_req)


class AIRoom:
	def __init__(self, ai_core):
		self.ai_mgr = AIMgr(ai_core, 'skills/mgr.md')

	def query(self, q):
		resp = self.ai_mgr.query(q)
		if resp['flag'] == 'text':
			yield resp['msg']
		else:
			yield resp['msg']
		return

# class AIHandlerX:
# 	def __init__(self, ai_core):
# 		conf = ajson.gracefulLoadJSON('config.json')
# 		self.ai_mgr = ai_core(context_len=15, id_='Manager', model='qwen2.5:7b')
# 		self.ai_mgr.set_api(conf['api'])
# 		self.ai_worker = ai_core(context_len=10, id_='Engineer', model='qwen2.5:7b')
# 		self.ai_worker.set_api(conf['api'])
# 		self.worker = None
# 		self.skills = None
	
# 	def _load_skills(self):
# 		skills = {}
# 		md_files = [f for f in os.listdir('skills') if f.lower().endswith('.md')]
# 		for fp in md_files:
# 			skill = rw.read_t8(os.path.join('skills', fp))
# 			skill_env = rw.read_t8(os.path.join('env', os.path.splitext(fp)[0] + '.yml'))
# 			skills[fp] = skill.replace('{SKILL_ENV}', skill_env)
# 		return skills
	
# 	def online(self):
# 		self.setup = SkillLoader().get_main()
# 		self.ai_mgr.query(self.setup, role='system')
# 		self.worker = worker.Worker('tmp')
# 		# self.skills = self._load_skills()
	
# 	def query(self, q):
# 		if q == '/flush':
# 			self.ai_mgr.flush_context()
# 			yield '😤 ' + 'Memory flushed!'
# 			return 
# 		elif q == '/dump':
# 			yield str(self.ai_mgr.dumps_context())
# 			return 

# 		resp = self.ai_mgr.query(q)
# 		if resp[:4] != '000+':
# 			yield '😤 ' + resp
# 		elif resp[:4] == '000+':
# 			usr_req = resp[4:]
# 			yield '🤔 ' + usr_req
			
			
# 			# skill_use = j_resp['skill']
# 			# 
# 			# self.ai_worker.query(self.skills[skill_use+'.md'], role='system')
# 			# j_resp2 = json.loads(self.ai_worker.query(j_resp['msg']))
# 			# 
# 			# yield '🧙 ' + j_resp2['msg']
# 			# 
# 			# if j_resp2['type'] == 1:
# 			# 	codes = j_resp2['cmd']
# 			# 	yield codes
# 			# 	# if input('Execute? (y)') == 'y':
# 			# 	# 	w.run(skill_use, codes)