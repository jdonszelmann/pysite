from .thread import Thread
from queue import Queue
from .attributedict import AttributeDict

 

_event = AttributeDict({
	"READY":("port","address")
})

event = AttributeDict({i:i for i in _event.keys()})

class Event:

	def __init__(self,handler,eventtype):
		if not eventtype in event:
			raise TypeError("event type must be [{}]".format(",".join(("event." + str(i) for i in event.keys()))))
		
		self.func = None
		self.handler = handler
		self.eventtype = eventtype

		self.pending = Queue()

		Thread(self.eventloop)

	def eventloop(self):

		while True:
			if not self.pending.empty():
				self.pending.get()(self)

	#couple function to this event with decorator
	def __call__(self, func):
		self.func = func
		self.handler.events[self.eventtype].append(self)
		return self

	def fire(self, info):
		self.info = AttributeDict(info)

		for i in _event[self.eventtype]:
			if i not in self.info:
				raise ValueError(
					"expected attribute '[{}]' to be in Event.info. "
					"cannot start event without this requirement. "
					"requirements for this event are {}".format(i,",".join(_event[self.eventtype]))
				)

		self.pending.put(self.func)

class EventHandler:
	def __init__(self):
		self.events = {key:[] for key in list(event)}

	def on(self,*args,**kwargs):
		return Event(self,*args,**kwargs)	

	def fire(self,eventtype:event,info:dict={}):
		if not eventtype in event:
			raise TypeError("event type must be [{}]".format(",".join(("event." + str(i) for i in event.keys()))))
		if not isinstance(info,dict):
			raise TypeError("info must be of type dict")

		for i in self.events[eventtype]:
			i.fire(info)