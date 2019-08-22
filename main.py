from flask import Flask, jsonify, request
from firestore import *
from pyotp import TOTP
import re
import os
import logging

SLACK_TOKEN = os.environ['SLACK_TOKEN']

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)


@app.route('/slash', methods=['POST'])
def slash():
    payload = {
        'text': ''
    }

    if request.form['token'] != SLACK_TOKEN:
        payload['text'] = 'Sorry, I did not understand your command.'
        return jsonify(payload)

    command = request.form['text'].split(' ')
    command_type = command[0]

    if command_type == 'add':
        name = command[1]
        token = command[2]

        name_normal = re.sub("[^A-Za-z0-9]+", "", name)
        add_new_token(token, name_normal)

        payload['text'] = f'Successfully set up token for {name_normal}'

        return jsonify(payload)

    if command_type == 'get':
        name = command[1]
        try:
            token = get_token(name)
            totp = TOTP(token)
            passcode = totp.now()

            payload['text'] = f'One time password for {name} is {passcode}'
        except:
            payload['text'] = "Error: Token doesn't exist."
        finally:
            return jsonify(payload)

    payload['text'] = 'Sorry, I did not understand your command'
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)