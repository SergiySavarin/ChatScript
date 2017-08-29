#! /usr/bin/env python
import socket
import sys

from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route('/<user_name>/<bot_name>', methods=['POST'])
def messaging(user_name, bot_name):
    return jsonify({
        'message': send_to_bot(
            user_name,
            bot_name,
            request.form.to_dict().get('message')
        )
    })


def send_to_bot(user_name, bot_name, message):
    client = cs_connect()
    client.sendall(chr(0).join([user_name, bot_name, message]) + chr(0))
    message = cs_receive_message(client)
    client.close()
    return message


def cs_connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1024))
    return client


def cs_receive_message(client):
    message = ''
    while True:
        chunk = client.recv(32)
        if not chunk:
            break
        message += chunk
    return message


def check_cs_status():
    try:
        client = cs_connect()
        client.close()
    except socket.error as err:
        if err.errno == 61:
            raise Exception(
                '\nPlease run first ChatScript service\n'
                '"./BINARIES/LinuxChatScript64" or '
                '"./BINARIES/MacChatScript"\n'
                'To run in background use:\n'
                '"./BINARIES/LinuxChatScript64 &" or '
                '"./BINARIES/MacChatScript &"'
            )


def run_console_mode():
    console_mode = lambda: (sys.argv[1] == '--console' or sys.argv[1] == '-c')
    if len(sys.argv) > 1 and console_mode():
        user_name = raw_input('> Enter your name: ')
        bot_name = raw_input('> Enter bot name: ')
        while True:
            message = raw_input('> ')
            if ':build' in message:
                bot_name = message.split(' ')[~0]
            print send_to_bot(user_name, bot_name, message)


if __name__ == '__main__':
    check_cs_status()
    run_console_mode()
    app.run(host='localhost', port=5024, debug=True)
