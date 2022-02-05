from flask import Flask
from threading import Thread

app = Flask('__name__')

@app.route('/')
def home():
    return """<a href="https://discordapp.com/oauth2/authorize?client_id=923321635971412040&permissions=4294967287&scope=bot%20applications.commands">Invite Bot"""

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
