#! /usr/bin/env python
import socket
import sys

from flask import Flask
from flask import jsonify


app = Flask(__name__)


def send_to_bot(user_name, bot_name, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1024))
    client.sendall(chr(0).join([user_name, bot_name, message]) + chr(0))

    message = ''
    while True:
        chunk = client.recv(32)
        if not chunk:
            break
        message += chunk
    client.close()

    return message


@app.route('/<user_name>/<bot_name>/<message>', methods=['POST'])
def messaging(user_name, bot_name, message):
    return jsonify({'message': send_to_bot(user_name, bot_name, message)})


if __name__ == '__main__':
    if len(sys.argv) > 1 and (sys.argv[1] == '--console' or sys.argv[1] == '-c'):
        user_name = raw_input('> Enter your name: ')
        bot_name = raw_input('> Enter bot name: ')
        while True:
            print send_to_bot(user_name, bot_name, raw_input('> '))

    app.run(host='localhost', port=5024, debug=True)
