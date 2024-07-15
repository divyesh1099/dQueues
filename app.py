from flask import Flask, request, jsonify
import nsq
import json
import requests

app = Flask(__name__)

# Mapping of queue names to task functions
queue_task_mapping = {
    'queue1': 'task_function1',
    'queue2': 'task_function2'
}

# Function to publish a message to NSQ
def publish_message(topic, message):
    # Ensure the topic is created
    requests.post(f'http://127.0.0.1:4151/topic/create?topic={topic}')
    
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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
