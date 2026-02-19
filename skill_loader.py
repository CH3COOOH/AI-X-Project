import azstd.file.rw as rw

class SkillLoader:
	def __init__(self):
		pass

	def get_main(self):
		return rw.read_t8('skills/manager.md')