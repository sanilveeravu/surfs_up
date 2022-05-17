from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello world'

@app.route('/test')
def test_world():
  return 'Now in test'
