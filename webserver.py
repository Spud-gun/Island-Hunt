import flask
from threading import Thread

app = flask.Flask("")

@app.route("/")
def home():
  return "OK!"

def run():
  app.run(host = "0.0.0.0", port = 8080)

def keep():
  t = Thread(target = run)
  t.start()
