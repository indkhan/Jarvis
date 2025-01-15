
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(config, to, subject, body):
    """Send email using configured SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = config['email']['address']
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(config['email']['smtp_server'], 
                         config['email']['smtp_port']) as server:
            server.starttls()
            server.login(config['email']['address'], 
                        config['email']['password'])
            server.send_message(msg)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
