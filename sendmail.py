import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import json

# Read JSON
with open("methods/smtp.json") as json_data_file:
    data = json.load(json_data_file)

# Get SMTP data
def getSMTPData():
    sender_email = data["sender_email"]
    pwd = data["password"]
    smtp = data["smtp_server"]
    port = data["port"]
    return sender_email, pwd, smtp, port

# Create secure connection with server and send email
def sendMail(receiver_email, receiver_email_copy, subject, body, filename):
    sender_email, pwd, smtp, port = getSMTPData()

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = receiver_email_copy

    # Create the plain-text and HTML version of your message
    html = body

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(html, "html")

    message.attach(MIMEText(html, 'html'))
    with open(filename, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(filename)
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
    message.attach(part)
    
    # toaddrs = [receiver_email] + receiver_email_copy.split(",")
    toaddrs = receiver_email.split(",") + receiver_email_copy.split(",")
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp, port) as server:
        server.starttls()
        server.login(sender_email, pwd)
        server.sendmail(
            sender_email, toaddrs, message.as_string()
        )
        server.quit()
    print('Email sent successfully')