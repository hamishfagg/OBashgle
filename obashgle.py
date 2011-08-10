import Omegle
import bash as Bash
from twisted.internet import reactor

class Handler:
	def __init__(self):
		self.bash = Bash.Bash()
		self.client = None

	def start(self):
		self.client = Omegle.Omegle(self, 0)
		print "Connecting..."
		self.client.connect()

	def on_connected(self, index):
		print "Connected to a stranger."
		self.bash.changeDir('~')
		self.sendPrompt()
		
	def on_message(self, index, message):
		print "Stranger: %s" % message
		#Handle the command
		if message.startswith('cd '):
			output = self.bash.changeDir(message)
		else:
			output = self.bash.runCmd(message)
		
		#print and send output if there is some
		if output != "" and output != '\n':
			self.client.sendMsg(output)
			print output
		self.sendPrompt()
	
	def on_typing(self, index):
		print "Stranger is typing"
	
	def on_stoppedTyping(self, index):
		print "Stranger has stopped typing"

	def on_recaptcha(self, index, url):
		print "Recaptcha required: %s" % url
		self.client.sendCaptcha(raw_input("Response: "))

	def on_recaptchaResponse(self, index, accepted):
		if accepted: print 'Recaptcha accepted!'
		else: print 'Recaptcha rejected!'

	def on_disconnected(self, index, reason):
		print "Stranger has disconnected\n"
		self.client.connect()

	def sendPrompt(self):
		self.client.sendMsg(self.bash.getPrompt())
		print self.bash.getPrompt()

if __name__ == "__main__":
	handler = Handler()
	handler.start()
	reactor.run()
