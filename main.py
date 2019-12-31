from flask import Flask, jsonify, request
from firestore import *
from pyotp import TOTP
import requests
import json
import re
import os
import logging

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_WEBHOOK = os.environ['SLACK_WEBHOOK']

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

        name_normal = re.sub("[^A-Za-z0-9-]+", "", name)
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

@app.route('/sms', methods=['GET', 'POST'])
def receive():
    sms_body = request.values.get('Body', None)

    message = {
        'text': sms_body
    }

    response = requests.post(
        SLACK_WEBHOOK,
        data = json.dumps(message),
        headers = {'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f'Request to Slack returned an error {response.status_code}, error response: {response.text}')

    return sms_body

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)