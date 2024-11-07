import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        # Load and verify environment variables
        self.email = os.getenv('GMAIL_ADDRESS')
        self.password = os.getenv('GMAIL_APP_PASSWORD')
        self.recipient = os.getenv('RECIPIENT_EMAIL')
        # Get CC recipients as comma-separated list
        self.cc_recipients = os.getenv('CC_RECIPIENTS', '').split(',')
        # Remove any empty strings and strip whitespace
        self.cc_recipients = [email.strip() for email in self.cc_recipients if email.strip()]
        
        # Verify all required variables are present
        if not all([self.email, self.password, self.recipient]):
            raise ValueError("Missing required environment variables. Please check your .env file.")
        
        print(f"Initialized with email: {self.email}")
        print(f"App password length: {len(self.password)} characters")
        print(f"Primary recipient: {self.recipient}")
        print(f"CC recipients: {', '.join(self.cc_recipients) if self.cc_recipients else 'None'}")
        
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(days=10)
        
    def send_email(self):
        if datetime.now() > self.end_time:
            print("10-day period completed. Stopping the script...")
            return schedule.CancelJob
            
        try:
            print(f"\nAttempting to send email at {datetime.now()}")
            print("1. Creating message...")
            
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.recipient
            if self.cc_recipients:
                msg['Cc'] = ', '.join(self.cc_recipients)
            msg['Subject'] = f"Automated Email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            body = "This is an automated email sent from Raspberry Pi."
            msg.attach(MIMEText(body, 'plain'))
            
            print("2. Connecting to SMTP server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            
            print("3. Starting TLS...")
            server.starttls()
            
            print("4. Attempting login...")
            server.login(self.email, self.password)
            
            print("5. Sending email...")
            # Combine all recipients for sending
            all_recipients = [self.recipient] + self.cc_recipients
            text = msg.as_string()
            server.sendmail(self.email, all_recipients, text)
            
            print("6. Closing connection...")
            server.quit()
            
            print(f"Email sent successfully at {datetime.now()}")
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication failed:")
            print(f"- Email used: {self.email}")
            print(f"- Password length: {len(self.password)}")
            print(f"- Error details: {str(e)}")
            raise
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise

def main():
    try:
        sender = EmailSender()
        
        # Schedule email to be sent every 6 hours
        schedule.every(6).hours.do(sender.send_email)
        
        print("\nAttempting to send first email...")
        # Send first email immediately
        sender.send_email()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
