from typing.re import Pattern
import re
from .thread import Thread

class Route:
	def __init__(self,path,routetype="get",params={}):
		if type(path)  == str:
			self.path = re.compile(path)
		elif type(path) == Pattern:
			self.path = path
		else:
			raise ValueError("path must be either string or regex")

		self.routetype = routetype
		self.routefunc = None

	def run(self,req,res):
		m = self.path.fullmatch(req.path)
		if m and req.reqtype.lower() == self.routetype.lower():
			req.params = [i for i in m.groups()]
			Thread(self.routefunc, args=(req,res))


	def __call__(self,routefunc):
		self.routefunc = routefunc
		return self