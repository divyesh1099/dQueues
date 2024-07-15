import nsq
import json

# Define the task functions
def task_function1(data):
    print(f"Executing task_function1 with data: {data}")
    # Add your task logic here

def task_function2(data):
    print(f"Executing task_function2 with data: {data}")
    # Add your task logic here

# Mapping of queue names to actual functions
task_mapping = {
    'queue1': task_function1,
    'queue2': task_function2
}

def task_handler(message):
    try:
        msg_content = json.loads(message.body.decode())
        queue_name = message.topic
        task_data = msg_content

        if queue_name in task_mapping:
            task_function = task_mapping[queue_name]
            task_function(task_data)
            return True
        else:
            print(f"No task assigned for queue: {queue_name}")
            return False
    except Exception as e:
        print(f"Error processing message: {e}")
        return False

def run_consumer():
    r = nsq.Reader(
        message_handler=task_handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='queue1',
        channel='channel1',
        lookupd_poll_interval=15
    )

    r2 = nsq.Reader(
        message_handler=task_handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='queue2',
        channel='channel2',
        lookupd_poll_interval=15
    )

    nsq.run()

if __name__ == "__main__":
    run_consumer()
