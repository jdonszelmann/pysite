

import json
import os
from .attributedict import AttributeDict, attributedict

class Config:

	default = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","defaultconfig.json")

	def __init__(self):
		self.loaddefault()

	def load(self,filename):
		with open(filename) as f:
			self.config = attributedict(json.load(f))

	def loaddefault(self):
		self.load(self.default)

	def __iter__(self):
		return self.config

	def __getattr__(self,attr):

		if attr in self.config:
			return self.config[attr]
		else:
			return self.__getattribute__(attr)

	def __contains__(self,item):
		return item in self.config

	def __repr__(self):
		return str(self.config)