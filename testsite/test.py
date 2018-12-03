import sys
sys.path.append("..")
import pysite

app = pysite.Website()


@app.route(r"/")
def index(req,res):
	res.send("hello world")

@app.route(r"/test")
def index(req,res):
	res.sendFile("test.html")


@app.on(pysite.event.READY)
def ready(event):
	print("server ready and listening on port {}".format(event.info.port))

app.listen(8000)