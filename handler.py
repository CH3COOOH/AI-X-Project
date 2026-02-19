import os
import json

import azstd.file.json as ajson
import azstd.file.rw as rw
from skill_loader import SkillLoader
import worker

class AIHandlerX:
	def __init__(self, ai_core):
		conf = ajson.gracefulLoadJSON('config.json')
		self.ai_mgr = ai_core(context_len=15, id_='Manager', model='qwen2.5:7b')
		self.ai_mgr.set_api(conf['api'])
		self.ai_worker = ai_core(context_len=10, id_='Engineer', model='qwen2.5:7b')
		self.ai_worker.set_api(conf['api'])
		self.worker = None
		self.skills = None
	
	def _load_skills(self):
		skills = {}
		md_files = [f for f in os.listdir('skills') if f.lower().endswith('.md')]
		for fp in md_files:
			skill = rw.read_t8(os.path.join('skills', fp))
			skill_env = rw.read_t8(os.path.join('env', os.path.splitext(fp)[0] + '.yml'))
			skills[fp] = skill.replace('{SKILL_ENV}', skill_env)
		return skills
	
	def online(self):
		self.setup = SkillLoader().get_main()
		self.ai_mgr.query(self.setup, role='system')
		self.worker = worker.Worker('tmp')
		# self.skills = self._load_skills()
	
	def query(self, q):
		if q == '/flush':
			self.ai_mgr.flush_context()
			yield '😤 ' + 'Memory flushed!'
			return 
		elif q == '/dump':
			yield str(self.ai_mgr.dumps_context())
			return 

		resp = self.ai_mgr.query(q)
		if resp[:4] != '000+':
			yield '😤 ' + resp
		elif resp[:4] == '000+':
			usr_req = resp[4:]
			yield '🤔 ' + usr_req
			
			
			# skill_use = j_resp['skill']
			# 
			# self.ai_worker.query(self.skills[skill_use+'.md'], role='system')
			# j_resp2 = json.loads(self.ai_worker.query(j_resp['msg']))
			# 
			# yield '🧙 ' + j_resp2['msg']
			# 
			# if j_resp2['type'] == 1:
			# 	codes = j_resp2['cmd']
			# 	yield codes
			# 	# if input('Execute? (y)') == 'y':
			# 	# 	w.run(skill_use, codes)