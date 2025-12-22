# DevOps 101 Labs - Lab 08: AWS Services

This lab demonstrates practical usage of AWS services through hands-on demos. You'll learn how to interact with Amazon S3 (Simple Storage Service), Amazon SQS (Simple Queue Service), and Amazon DynamoDB (NoSQL Database) using Python and the AWS SDK.

## Prerequisites

### AWS CLI v2 Installation

The [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/) is a powerful tool that allows interaction with AWS services directly from the terminal.

**AWS CLI version 2** is required for this lab for several reasons:

- **SSO Authentication:** Version 2 adds support for AWS Single Sign-On (SSO), allowing the use of secure, short-lived credentials and convenient switching between development and production accounts.
- **Improved Features:** AWS CLI v2 offers enhanced features, such as improved autocomplete, advanced JSON output formatting, and full support for the latest AWS services and endpoints.
- **Better Cross-Platform Support:** It includes official installers for Linux and MacOS, and provides bug fixes and security improvements over v1.

> **Note:** AWS CLI v1 does *not* support SSO login flows and is missing several features required by the workflow. AWS CLI v2 should be installed or upgraded following the steps below.

#### Install AWS CLI v2 on Linux

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install -i ~/.local/aws-cli -b ~/.local/bin
```

### Python Environment Setup

This project uses `uv` for dependency management. Set up the virtual environment:

* Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* Create and activate venv
```bash
uv venv
source .venv/bin/activate
```

* Install dependencies

```bash
uv sync
```

## Labs Overview

This repository contains three hands-on demos:

### [Lab 01: S3 Demo](./01_s3/)

Learn how to interact with Amazon Simple Storage Service (S3) through a Streamlit web application. This demo covers:

- Uploading images to S3 buckets
- Listing and previewing stored images
- Deleting objects from S3
- Working with S3 API operations (PutObject, ListObjectsV2, GetObject, DeleteObject)

**Get started:** See the [S3 Demo README](./01_s3/readme.md) for detailed instructions.

### [Lab 02: SQS Demo](./02_sqs/)

Learn how to use Amazon Simple Queue Service (SQS) for message queuing. This demo covers:

- Creating and configuring SQS queues
- Sending messages to queues
- Receiving and processing messages with a worker
- Understanding queue attributes (VisibilityTimeout, MessageRetentionPeriod, Long Polling)

**Get started:** See the [SQS Demo README](./02_sqs/readme.md) for detailed instructions.

### [Lab 03: DynamoDB Demo](./03_dynamodb/)

Learn how to use Amazon DynamoDB for NoSQL database operations. This demo covers:

- Creating DynamoDB tables
- Adding, reading, updating, and deleting items
- Working with partition keys and attributes
- Understanding on-demand billing mode
- Building a task manager application

**Get started:** See the [DynamoDB Demo README](./03_dynamodb/readme.md) for detailed instructions.

## Project Structure

```
.
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── uv.lock                # Dependency lock file
├── 01_s3/                 # S3 demo application
│   ├── readme.md         # S3 demo instructions
│   ├── app.py            # Streamlit web interface
│   └── s3_utils.py       # S3 utility functions
├── 02_sqs/               # SQS demo application
    ├── readme.md         # SQS demo instructions
    ├── app.py            # Streamlit message sender
    ├── worker.py         # Message processor worker
    └── sqs_utils.py      # SQS utility functions
└── 03_dynamodb/          # DynamoDB demo application
    ├── readme.md         # DynamoDB demo instructions
    ├── app.py            # Streamlit task manager interface
    └── dynamodb_utils.py # DynamoDB utility functions
```

## Technologies Used

- **Python 3.13+**: Programming language
- **boto3**: AWS SDK for Python
- **Streamlit**: Web application framework for building UIs
- **uv**: Fast Python package installer and resolver

