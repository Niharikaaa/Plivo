# Plivo
Case Assessment 
This project implements a multi-level IVR system using the Plivo Voice API and Python Flask.

## Prerequisites
1. Python 3.8.8
2. Plivo Account
3. Ngrok

## Setup
1. Install dependencies: `pip install plivo flask`
2. Update `make_call.py` with your Plivo Credentials.
3. Run the server: `python ivr_app.py`
4. Expose the server: `ngrok http 8080`
5. Trigger the call: `python make_call.py`
