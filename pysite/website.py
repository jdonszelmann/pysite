
from http.server import *
import threading

from . import route
from . import config
from . import requesthandler
from . import events
from .thread import Thread

class Website:
	def __init__(self):
		self.config = config.Config()
		self.routes = []
		self.eventhandler = events.EventHandler()
		self.server = None
		self.port = None
		self.address = None

	def route(self,*args,**kwargs):
		r = route.Route(*args,**kwargs)
		self.routes.append(r)
		return r

	def on(self,*args,**kwargs):
		return self.eventhandler.on(*args,**kwargs)

	def listen(self,port=None, address=None):
		if port == None:
			if "server" in self.config and "port" in self.config.server:
				port = self.config.server.port
			else:
				raise ValueError("no port specified")

		if address == None:
			if "server" in self.config and "address" in self.config.server:
				address = self.config.server.address
			else:
				raise ValueError("no address specified")


		self.port = port
		self.address = address
		

		self.server = HTTPServer((address, port), requesthandler.RequestHandler)
		self.server.handler = self

		# server.socket = ssl.wrap_socket (httpd.socket, 
		# 	keyfile="path/to/key.pem", 
		# 	certfile='path/to/cert.pem', server_side=True)
		Thread(self.server.serve_forever)

		self.eventhandler.fire(events.event.READY,{"port":self.port,"address":self.address})
		while True:
			pass

	def handleREQ(self,req,res):
		print(req,res)
		for i in self.routes:
			i.run(req,res)
		res.tryEnd()
