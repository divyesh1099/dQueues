# dQueues/app.py
from flask import Flask, request, jsonify
import nsq
import json
import requests
from queues.send_email import send_email
from utils import get_system_uptime

app = Flask(__name__)

# Mapping of queue names to task functions
queue_task_mapping = {
    'send_gmail': 'send_gmail',
    'send_outlook': 'send_outlook',
    # Add other queues here if needed
}

# Function to publish a message to NSQ
def publish_message(topic, message):
    # Ensure the topic is created
    response = requests.post(f'http://127.0.0.1:4151/topic/create?topic={topic}')
    if response.status_code != 200:
        print(f"Error creating topic {topic}: {response.text}")
    
    writer = nsq.Writer(['127.0.0.1:4150'])

    def pub_callback(conn, data):
        print(f"Message sent to NSQ: {data}")

    writer.pub(topic, json.dumps(message), pub_callback)

@app.route('/enqueue', methods=['POST'])
def enqueue():
    data = request.json
    queue_name = data.get('queue_name')
    task_data = data.get('task_data')

    if queue_name in queue_task_mapping:
        publish_message(queue_name, task_data)
        return jsonify({"status": "success", "message": "Task enqueued"}), 200
    else:
        return jsonify({"status": "error", "message": "Not a valid queue"}), 400
    
@app.route('/uptime', methods=['GET'])
def uptime():
    uptime_info = get_system_uptime()
    return jsonify(uptime_info), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
