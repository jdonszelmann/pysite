
import threading
import time

class Thread(threading.Thread):

	threads = []
	threadlimit = 10

	def __init__(self,func, args=()):
		if not callable(func):
			raise TypeError("thread must run a function")

		self.func = func
		self.args = args

		while len(self.__class__.threads) > self.__class__.threadlimit:
			time.sleep(0.01)

		self.__class__.threads.append(self)

		super().__init__()
		self.daemon = True
		self.start()

	@classmethod
	def setThreadLimit(cls,limit):
		cls.threadlimit = limit

	def run(self):
		self.func(*self.args)

setThreadLimit = Thread.setThreadLimit