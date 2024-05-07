import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime
import getpass
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'shivanprasad1@gmail.com'

class EmailApp:
    def __init__(self, master):
        self.master = master
        master.title("Email Daily Report")

        self.label_sender = tk.Label(master, text="Your Email Address:")
        self.label_sender.grid(row=0, column=0, sticky=tk.W)
        self.entry_sender = tk.Entry(master)
        self.entry_sender.grid(row=0, column=1)

        self.label_receiver = tk.Label(master, text="Recipient's Email Address:")
        self.label_receiver.grid(row=1, column=0, sticky=tk.W)
        self.entry_receiver = tk.Entry(master)
        self.entry_receiver.grid(row=1, column=1)

        self.label_body = tk.Label(master, text="Email Content:")
        self.label_body.grid(row=2, column=0, sticky=tk.W)
        self.text_body = tk.Text(master, width=50, height=10)
        self.text_body.grid(row=2, column=1)

        self.label_attachment = tk.Label(master, text="Attachment File(s):")
        self.label_attachment.grid(row=3, column=0, sticky=tk.W)
        self.entry_attachment = tk.Entry(master, state='readonly')
        self.entry_attachment.grid(row=3, column=1)
        self.button_browse = tk.Button(master, text="Browse", command=self.browse_attachment)
        self.button_browse.grid(row=3, column=2)

        self.button_send = tk.Button(master, text="Send Email", command=self.send_email)
        self.button_send.grid(row=4, column=0, columnspan=3)

    def browse_attachment(self):
        file_paths = filedialog.askopenfilenames()
        self.entry_attachment.config(state='normal')
        self.entry_attachment.delete(0, tk.END)
        self.entry_attachment.insert(0, '; '.join(file_paths))
        self.entry_attachment.config(state='readonly')

    def send_email(self):
        sender_email = self.entry_sender.get()
        receiver_email = self.entry_receiver.get()
        body = self.text_body.get("1.0", tk.END)

        # Generate daily report
        report = generate_daily_report()

        # Print app password guide
        print_app_password_guide()

        # Prompt for app password
        smtp_password = simpledialog.askstring("App Password", "Enter your App Password:")

        # Get attachment paths
        attachment_paths = self.entry_attachment.get().split(';') if self.entry_attachment.get() else []

        # Send email
        send_email(sender_email, receiver_email, "Daily Report", report + body, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, smtp_password, attachment_paths)

        # Show confirmation message
        messagebox.showinfo("Email Sent", "Your daily report email has been sent!")

def generate_daily_report():
    # Your report generation logic here
    today = datetime.date.today()
    report = f"Daily Report - {today}\n\n"
    return report

def prepare_email(sender_email, receiver_email, subject, body, attachment_paths=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_paths:
        for attachment_path in attachment_paths:
            # Open each file to be attached
            with open(attachment_path.strip(), 'rb') as attachment:
                # Add file as application/octet-stream
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path.strip())}',
            )

            # Add attachment to message
            msg.attach(part)

    return msg.as_string()

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password, attachment_paths=None):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, prepare_email(sender_email, receiver_email, subject, body, attachment_paths))
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def print_app_password_guide():
    print("To use this program, you need to generate an 'App Password' for your email account.")
    print("Here's how you can generate an App Password:")
    print("1. Go to your email account's security settings.")
    print("2. Look for the option to generate an App Password.")
    print("3. Select the option and follow the prompts to generate a new App Password.")
    print("4. Copy the generated App Password and use it as the password when prompted by this program.")

def main():
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
