Image Processing System


Overview

This project processes images asynchronously from a CSV file, compressing them by 50% and storing the results in an SQL Server database. It provides APIs for file upload, processing status checks, and webhook notifications.


Tech Stack

Backend: Python (Flask, Celery)

Database: SQL Server

Message Queue: Redis (for asynchronous processing)

Image Processing: Pillow (PIL)

Storage: Local 


Features

Accepts CSV file with product details and image URLs

Validates CSV format

Asynchronously processes images (compression by 50%)

Stores input/output image URLs in the database

Provides an API to check processing status

Sends a webhook notification upon completion


Project Structure

image_processing_project/
│── app.py                  # Flask API server
│── database.py              # SQL Server connection
│── worker.py                # Celery worker for async processing
│── webhook.py               # Webhook handler
│── requirements.txt         # Dependencies
│── uploads/                 # Directory for storing CSVs (if needed)
│── processed_images/        # Directory for output images (if local storage)
└── schema.sql               # SQL script to create tables


Installation

Install Dependencies

pip install -r requirements.txt


Set Up SQL Server Database

Ensure SQL Server is running

Update database.py with your database credentials


Start Redis

redis-server


Start Flask API Server

python app.py


Start Celery Worker

celery -A worker worker --loglevel=info


API Endpoints

Upload CSV (POST /upload)


Method: POST

URL: http://127.0.0.1:5000/upload

Body: Form-data (CSV file upload)

Response: { "request_id": "UUID" }

Check Status (GET /status/{request_id})


Method: GET

URL: http://127.0.0.1:5000/status/{request_id}

Response: { "status": "Pending | Processing | Completed" }

Webhook Notification

Triggered when processing completes

Payload: { "request_id": "UUID", "status": "Completed", "output_images": [...] }
