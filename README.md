
# dQueues Project

## Overview

The `dQueues` project is a message queuing system using NSQ for task processing. It allows you to enqueue tasks, which are then processed by consumers. This project includes functionality to send emails via Gmail and Outlook, and also provides an endpoint to check the system uptime of the server it's deployed on.

## Features

- **Enqueue tasks**: Send tasks to NSQ for processing.
- **Email sending**: Send emails using Gmail or Outlook.
- **System uptime**: Check if the server is running and when it was last booted.

## Technologies Used

- **Python**: The core programming language used for the Flask web application and task consumers.
- **Flask**: A micro web framework used to create the web application.
- **NSQ**: A real-time distributed messaging platform used as the message broker.
- **psutil**: A Python library used to fetch system uptime information.

## Project Structure

```
dQueues/
├── app.py                  # The main Flask application
├── consumer.py             # Consumer script to process NSQ messages
├── queues/
│   ├── __init__.py
│   ├── send_email.py       # Email sending functionality
│   └── other_queue.py      # Placeholder for other queues
├── utils.py                # Utility functions, including system uptime
├── config.py               # Configuration for email accounts and SMTP settings
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation
```

## How to Run the Project

### Prerequisites

1. **Python**: Ensure Python is installed. You can download it from [Python's website](https://www.python.org/downloads/).
2. **Git**: Ensure Git is installed. You can download it from [Git's website](https://git-scm.com/download/win).
3. **NSQ**: Download NSQ binaries from the [NSQ GitHub releases page](https://github.com/nsqio/nsq/releases) and extract them to a directory (e.g., `C:\nsq`).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd dQueues
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Edit `config.py` to add your email credentials and SMTP settings.

```python
# dQueues/config.py
EMAIL_CONFIG = {
    'senders': {
        'your-gmail-email@gmail.com': 'your-gmail-app-password',
        'your-outlook-email@outlook.com': 'your-outlook-app-password'
    },
    'smtp_settings': {
        'gmail': {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587
        },
        'outlook': {
            'smtp_server': 'smtp.office365.com',
            'smtp_port': 587
        }
    }
}
```

### Running the Project

1. **Start NSQ Components**:
   Open three Command Prompt windows and run the following commands:

   **Window 1: Start nsqlookupd**:
   ```bash
   cd C:\nsq
   nsqlookupd
   ```

   **Window 2: Start nsqd**:
   ```bash
   cd C:\nsq
   nsqd --lookupd-tcp-address=127.0.0.1:4160
   ```

   **Window 3: Start nsqadmin**:
   ```bash
   cd C:\nsq
   nsqadmin --lookupd-http-address=127.0.0.1:4161
   ```

2. **Run the Flask Application**:
   In a new Command Prompt window, navigate to the project directory and run:
   ```bash
   python app.py
   ```

3. **Run the Consumer**:
   In another Command Prompt window, navigate to the project directory and run:
   ```bash
   python consumer.py
   ```

### API Endpoints

#### Enqueue Task

**Endpoint**: `/enqueue`  
**Method**: `POST`  
**Description**: Enqueue a task to send an email.

**Request Body**:
```json
{
  "queue_name": "send_gmail" or "send_outlook",
  "task_data": {
    "sender_email": "your-email",
    "receivers": ["receiver-email"],
    "subject": "Email Subject",
    "body": "Email Body",
    "body_type": "plain" or "html",
    "attachments": [
      {
        "filename": "file.txt",
        "filepath": "path/to/file.txt"
      }
    ]
  }
}
```

#### Check System Uptime

**Endpoint**: `/uptime`  
**Method**: `GET`  
**Description**: Get the system uptime information.

**Response**:
```json
{
  "boot_time": "2024-07-15 09:35:17",
  "uptime": "1 day, 2:14:35.123456"
}
```

### NSQ Overview

**NSQ** is a real-time messaging platform that allows you to decouple your applications using message queues. It consists of:

- **nsqd**: The daemon that receives, queues, and delivers messages to clients.
- **nsqlookupd**: The daemon that manages topology information about nsqd instances.
- **nsqadmin**: A web-based admin interface to view message statistics.

In this project, NSQ is used to queue tasks for sending emails. The Flask application enqueues tasks to NSQ, and consumers process these tasks by sending the emails.

### Usage

1. Start all the NSQ components.
2. Run the Flask application.
3. Use the `/enqueue` endpoint to send tasks to the queue.
4. The consumer picks up tasks from the queue and processes them.

### Contributing

Feel free to contribute to this project by submitting issues or pull requests. Please ensure that your contributions align with the project's objectives.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Feel free to reach out if you have any questions or need further assistance!
