import subprocess
import threading
import queue
import time

import azstd.file.rw as rw

class Interpreter:
	def __init__(self):
		self.buf = [None, None]
	
	def __read(self, fpath):
		try:
			self.buf[0] = rw.read_t8(fpath)
			self.buf[1] = '0'
			print('OK')
		except Exception as e:
			print(e)
			self.buf[1] = '1'
	
	def __write(self, fpath):
		try:
			rw.write_t8(fpath, self.buf[0])
			self.buf[1] = '0'
			print('OK')
		except Exception as e:
			print(e)
			self.buf[1] = '1'
	
	def __mov(self, buf_n, value):
		self.buf[buf_n] = value
		print('OK')
	
	def __exec(self, cmdline):
		print(cmdline)


	def interpret(self, cmd):
		cmd_ctrl = cmd[:4]
		cmd_param = cmd[5:]
		if cmd_ctrl == '0000':
			self.__mov(0, cmd_param)
		elif cmd_ctrl == '0001':
			self.__read(cmd_param)
		elif cmd_ctrl == '0002':
			self.__write(cmd_param)
		elif cmd_ctrl == '0003':
			self.__exec(cmd_param)
		else:
			print(f'Invalid command: {cmd_ctrl}')
		
if __name__ == '__main__':
	iptr = Interpreter()
	while True:
		cmd = input('> ')
		if cmd == '':
			continue
		iptr.interpret(cmd)