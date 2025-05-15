# Description: This is a simple Flask server that returns a test message.
# Author: Filipe Carvalho

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is a test!"

if __name__ == '__main__':
    app.run(debug=True)
