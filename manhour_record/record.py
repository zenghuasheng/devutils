import json
import os
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)


def get_filename_by_date(date):
    return f'{date}.json'


def get_today_filename():
    today = datetime.now().strftime('%Y-%m-%d')
    return f'{today}.json'


def save_task_key(task_key):
    # 去掉 task- 前缀
    task_key = task_key[5:]
    filename = get_today_filename()

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = []

    if task_key not in data:
        data.append(task_key)
        with open(filename, 'w') as file:
            json.dump(data, file)


@app.route('/intercepted-request', methods=['OPTIONS', 'POST'])
def intercepted_request():
    if request.method == 'OPTIONS':
        response = app.response_class()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    data = request.json
    try:
        request_body = json.loads(data['requestBody'])
        task_key = request_body['variables']['key']
        print(task_key)
        save_task_key(task_key)
    except (KeyError, json.JSONDecodeError) as e:
        print('Error extracting task_key:', e)

    response = jsonify({"status": "success"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get-task-keys', methods=['GET'])
def get_task_keys():
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    filename = get_filename_by_date(date)

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = []

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(port=5050)
