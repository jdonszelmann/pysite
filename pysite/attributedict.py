



class AttributeDict(dict):
	def __init__(self, dictionary={}):
		super().__init__(dictionary)

	def __getattr__(self,attr):
		if attr in self:
			return self[attr]
		else:
			self.__getattribute__(attr)


def attributedict(dictionary):
	res = AttributeDict()

	for key,value in dictionary.items():
		if type(value) == dict:
			res[key] = attributedict(value)
		else:
			res[key] = value

	return res