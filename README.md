# Email Daily Report

This program enables users to send a daily report via email, featuring a simple graphical interface built using Tkinter in Python.

## Features
- Send daily reports via email.
- Include attachments in the email.
- Easy-to-use graphical interface.

## Requirements
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- smtplib module
- email module

## Setup
1. Ensure you have Python installed on your system.
2. Install the required modules using pip:
    ```bash
    pip install smtplib
    pip install email
    ```
3. Update the SMTP server details in the program (`SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`).
4. Enable less secure apps access in your email account or generate an App Password.
5. Replace `SMTP_USERNAME` with your email address.

## Usage
1. Run the program by executing the `main.py` file.
2. Enter your email address, recipient's email address, email content, and attach files if needed.
3. Click on the "Send Email" button.
4. Follow the prompt to enter your App Password.
5. Once sent, a confirmation message will appear.

## Note
- It's recommended to use a dedicated email address for sending reports.
- Ensure that your email provider supports SMTP.
