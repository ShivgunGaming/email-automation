import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'shivanprasad1@gmail.com'

class EmailApp:
    def __init__(self, master):
        self.master = master
        master.title("Email Daily Report")

        self.frame = tk.Frame(master, bg="#f0f0f0", padx=20, pady=20, bd=2, relief=tk.GROOVE)
        self.frame.pack()

        self.label_sender = tk.Label(self.frame, text="Your Email Address:", bg="#f0f0f0", font=("Arial", 12))
        self.label_sender.grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.entry_sender = tk.Entry(self.frame, font=("Arial", 12), bd=2, relief=tk.SOLID)
        self.entry_sender.grid(row=0, column=1, padx=(0, 10), pady=5, sticky=tk.W+tk.E)

        self.label_receiver = tk.Label(self.frame, text="Recipient's Email Address:", bg="#f0f0f0", font=("Arial", 12))
        self.label_receiver.grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.entry_receiver = tk.Entry(self.frame, font=("Arial", 12), bd=2, relief=tk.SOLID)
        self.entry_receiver.grid(row=1, column=1, padx=(0, 10), pady=5, sticky=tk.W+tk.E)

        self.label_body = tk.Label(self.frame, text="Email Content:", bg="#f0f0f0", font=("Arial", 12))
        self.label_body.grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.text_body = tk.Text(self.frame, width=50, height=10, font=("Arial", 12), bd=2, relief=tk.SOLID)
        self.text_body.grid(row=2, column=1, padx=(0, 10), pady=5, sticky=tk.W+tk.E)

        self.label_attachment = tk.Label(self.frame, text="Attachment File(s):", bg="#f0f0f0", font=("Arial", 12))
        self.label_attachment.grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.entry_attachment = tk.Entry(self.frame, state='readonly', font=("Arial", 12), bd=2, relief=tk.SOLID)
        self.entry_attachment.grid(row=3, column=1, padx=(0, 10), pady=5, sticky=tk.W+tk.E)
        self.button_browse = tk.Button(self.frame, text="Browse", command=self.browse_attachment, font=("Arial", 10), bg="#4CAF50", fg="white", padx=5)
        self.button_browse.grid(row=3, column=2, pady=5)

        self.label_password = tk.Label(self.frame, text="SMTP Password:", bg="#f0f0f0", font=("Arial", 12))
        self.label_password.grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.entry_password = tk.Entry(self.frame, show="*", font=("Arial", 12), bd=2, relief=tk.SOLID)
        self.entry_password.grid(row=4, column=1, padx=(0, 10), pady=5, sticky=tk.W+tk.E)

        self.button_send = tk.Button(self.frame, text="Send Email", command=self.send_email, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10)
        self.button_send.grid(row=5, column=0, columnspan=3, pady=10)

        self.button_clear = tk.Button(self.frame, text="Clear", command=self.clear_fields, font=("Arial", 12), bg="#f44336", fg="white", padx=10)
        self.button_clear.grid(row=6, column=0, columnspan=3, pady=10)

        # Add logo
        self.logo = tk.PhotoImage(file="email-logo.png")
        self.logo_label = tk.Label(self.frame, image=self.logo, bg="#f0f0f0")
        self.logo_label.grid(row=0, column=3, rowspan=4, padx=10)

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
        smtp_password = self.entry_password.get()

        if not all([sender_email, receiver_email, body, smtp_password]):
            messagebox.showwarning("Missing Information", "Please fill in all required fields.")
            return

        # Generate daily report
        report = generate_daily_report()

        # Get attachment paths
        attachment_paths = self.entry_attachment.get().split(';') if self.entry_attachment.get() else []

        # Send email
        send_email(sender_email, receiver_email, "Daily Report", report + body, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, smtp_password, attachment_paths)

    def clear_fields(self):
        self.entry_sender.delete(0, tk.END)
        self.entry_receiver.delete(0, tk.END)
        self.text_body.delete("1.0", tk.END)
        self.entry_attachment.config(state='normal')
        self.entry_attachment.delete(0, tk.END)
        self.entry_attachment.config(state='readonly')
        self.entry_password.delete(0, tk.END)

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
        messagebox.showinfo("Email Sent", "Your daily report email has been sent!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
