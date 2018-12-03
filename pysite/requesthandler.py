from http.server import *
from urllib.parse import urlparse, parse_qsl

class Request:
	def __init__(self,handler):
		self._handler = handler

		self.adress = handler.client_address[0]
		self.port = handler.client_address[1]
		self.reqtype = handler.command
		self.protocol = handler.protocol_version

		self._headers = handler.headers
		if hasattr(handler,"body"):
			self.body = handler.body
		else:
			self.body = None

		try:
			content_length = int(handler.headers['Content-Length'])
			self.data = handler.rfile.read(content_length)
		except TypeError:
			self.data = None


		url = urlparse(handler.path)
		self.path = url.path
		self.query = dict(parse_qsl(url.query))
		self.params = []

		self.website = handler.server.handler

	@property
	def headers(self):
		return self._headers
	

	def __repr__(self):
		return "{}:{{{}}}".format(self.__class__.__name__,",".join(["{}:{}".format(key,value) for key,value in self.__dict__.items() if not key.startswith("_") and not callable(getattr(self,key))]))

class Response:
	def __init__(self,handler):
		self._handler = handler
		self.website = handler.server.handler

		self._headerssent = False
		self._response = b""
		self._statuscode = 404
		self._contenttype = ""

	def end(self):
		self._handler.send_response(self._statuscode)
		self._handler.send_header('Content-type', self._contenttype)
		self._handler.end_headers()
		self._handler.wfile.write(self._response)

		self._handler.end_headers()
		self._headerssent = True

	def tryEnd(self):
		if not self._headerssent:
			self.end()

	def headersSent(self):
		return self._headerssent

	def status(self,code):
		self._statuscode = code

	def redirect(self,url):
		pass

	# def render(self)

	def content(self,contenttype):
		self._contenttype = contenttype

	def send(self,*args,mimetype="text/plain",**kwargs):
		self.content(mimetype)
		self._send(*args,**kwargs)

	def _send(self,body):
		#add json send when body is dict/array
		self.status(200)
		if type(body) == str:
			self._response += body.encode("utf-8")
		elif type(body) == bytes:
			self._response += body
		else:
			self._response += str(body).encode("utf-8")

	def sendFile(self,path, *args, mimetype="text/html",**kwargs):
		self.content(mimetype)
		with open(path) as f:
			self._send(f.read(), *args, **kwargs)

	def __repr__(self):
		return "{}:{{{}}}".format(self.__class__.__name__,",".join(["{}:{}".format(key,value) for key,value in self.__dict__.items() if not key.startswith("_") and not callable(getattr(self,key))]))


class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.server.handler.handleREQ(Request(self),Response(self))

		# self.send_response(200)
		# self.send_header('Content-type', 'text/html')
		# self.end_headers()
		# self.wfile.write(b'Hello, world!')


	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_POST(self):
		length = int(self.headers['Content-Length']) # <--- Gets the size of data
		self.body = self.rfile.read(length).decode("utf-8") # <--- Gets the data itself


		self.server.handler.handleREQ(Request(self),Response(self))


		# logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
		# str(self.path), str(self.headers), post_data.decode('utf-8'))

  #       self.send_response(200)
  #       self.send_header('Content-type', 'text/html')
  #       self.end_headers()
		# self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

	def log_message(self, format, *args):
		return

