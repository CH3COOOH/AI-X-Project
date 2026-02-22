import subprocess
import threading
import shlex
import time

class Exec:
	def __init__(self, log_encoding='ansi'):
		self.log_encoding = log_encoding
		self.process = None
		self.out = []
	
	def run(self, cmd, isPrint=False, isRecord=False):
		cmd_ = shlex.split(cmd, posix=True)
		self.process = subprocess.Popen(
				cmd_,
				shell=False,
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT,
				text=True,
				encoding=self.log_encoding,
				errors="ignore",
				bufsize=4096
			)
		for line in self.process.stdout:
			line_out = line.strip()
			if isPrint == True:
				print(line_out)
			if isRecord == True:
				self.out.append(line_out)
		self.process.wait()
		
		if isRecord == True:
			sout = '\n'.join(self.out)
			self.out = []
			return sout
		else:
			return ''
	
	def run_with_timeout(self, cmd, timeout, sampling=0.5):
		th = threading.Thread(target=self.run, args=(cmd, False, True, ))
		th.start()
		ts = time.time()
		while True:
			time.sleep(sampling)
			if self.process.poll() != None:
				break
			dt = time.time() - ts
			if dt > timeout:
				print('Process timeout, terminate forcely.')
				self.process.terminate()
				break
		sout = '\n'.join(self.out)
		self.out = []
		return sout

if __name__ == '__main__':
	e = Exec()
	print('isPrint=True, isRecord=False')
	print(e.run('ping 127.0.0.1 -n 10', isPrint=True, isRecord=False))
	print('isPrint=False, isRecord=True')
	print(e.run('ping 127.0.0.1 -n 10', isPrint=False, isRecord=True))
	print('run_with_timeout')
	print(e.run_with_timeout('ping 127.0.0.1 -n 10', 5))