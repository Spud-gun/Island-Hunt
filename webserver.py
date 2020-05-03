import flask
from threading import Thread

app = flask.Flask("")

@app.route("/")
def home():
  return "Yay! The bot is up and running! <p1>Logged in as Island Hunt#6349</p>"

def run():
  app.run(host = "0.0.0.0", port = 8080)

def keep():
  t = Thread(target = run)
  t.start()
