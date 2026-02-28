import sys_exec
import azstd.file.rw as rw

class Interpreter:
	def __init__(self):
		self.buf = [None, None]
		self.exec = sys_exec.Exec()
	
	def __read(self, fpath):
		try:
			self.buf[0] = rw.read_t8(fpath)
			self.buf[1] = '0'
			print('OK')
			return self.buf[0]
		except Exception as e:
			print(e)
			self.buf[1] = '1'
			return '** ERROR: READ'
	
	def __write(self, fpath):
		try:
			rw.write_t8(fpath, self.buf[0])
			self.buf[1] = '0'
			print('OK')
			return 'OK: ' + fpath
		except Exception as e:
			print(e)
			self.buf[1] = '1'
			return '** ERROR: WRITE'
	
	def __mov(self, buf_n, value):
		self.buf[buf_n] = value
		print('OK')
		return 'OK'
	
	def __exec(self, cmdline):
		print(cmdline)
		return self.exec.run(cmdline)

	def interpret(self, cmd):
		cmd_ctrl = cmd[:4]
		cmd_param = cmd[5:]
		if cmd_ctrl == '0000':
			return self.__mov(0, cmd_param)
		elif cmd_ctrl == '0001':
			return self.__read(cmd_param)
		elif cmd_ctrl == '0002':
			return self.__write(cmd_param)
		elif cmd_ctrl == '0003':
			return self.__exec(cmd_param)
		else:
			print(f'Invalid command: {cmd_ctrl}')
			return f'Invalid command: {cmd_ctrl}'

	def split(self, cmd_lines):
		blocks = []
		current = []

		for line in cmd_lines.splitlines():
			if re.match(r'^\d{4}\s+', line):
				if current:
					blocks.append("\n".join(current))
				current = [line]
			else:
				current.append(line)

		if current:
			blocks.append("\n".join(current))

		return blocks
		
if __name__ == '__main__':
	iptr = Interpreter()
	while True:
		cmd = input('> ')
		if cmd == '':
			continue
		iptr.interpret(cmd)