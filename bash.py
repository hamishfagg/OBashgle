import subprocess
from twisted.internet import reactor

class Bash:
	def __init__(self):
		self.workingDir = None
		self.homeDir = None
		self.changeDir('~')
		self.homeDir = self.workingDir
		self.shortDir = '~'

	def getPrompt(self):
		return "[guest@omegle %s]$" % self.shortDir	

	def runCmd(self, cmd):
		output, blah = subprocess.Popen(r'%s' % cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.workingDir).communicate()
		return output

	def changeDir(self, dir):
		if dir.startswith('cd '): dir = dir[3:]
		
		obj = subprocess.Popen(r'cd %s; echo $PWD; echo ${PWD##*/}' % dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.workingDir)
		output, blah = obj.communicate()
		
		if output.count('\n') == 2:
			dirs = output.split('\n')
			self.workingDir = dirs[0]
			self.shortDir = dirs[1]
			if self.workingDir == self.homeDir: self.shortDir = '~'
			if self.workingDir == '/': self.shortDir = '/'
			return None
		else:
			err = output.split('\n')[0:-3]
			return '\n'.join(err) + '\n'
