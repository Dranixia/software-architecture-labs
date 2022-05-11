from flask import Flask, request
import sys

app = Flask(__name__)


@app.route('/messages', methods=['GET', 'POST'])
def mess_requests():
    return "This is not implemented yet, sorry"


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
