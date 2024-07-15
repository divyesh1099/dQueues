# dQueues/consumer.py
import nsq
import json
from queues.send_email import send_email

# Mapping of queue names to actual functions
task_mapping = {
    'send_gmail': send_email,
    'send_outlook': send_email,
    # Add other queues here
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
    r1 = nsq.Reader(
        message_handler=task_handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='send_gmail',
        channel='email_channel',
        lookupd_poll_interval=15
    )

    r2 = nsq.Reader(
        message_handler=task_handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='send_outlook',
        channel='email_channel',
        lookupd_poll_interval=15
    )

    nsq.run()

if __name__ == "__main__":
    run_consumer()
