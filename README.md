# Gmail Automation for Raspberry Pi
A Python script to automate sending emails via Gmail at regular intervals using a Raspberry Pi. This solution enables scheduling emails to be sent every 6 hours for 10 days, with support for multiple recipients.

## Features
- 📧 Automated email sending every 6 hours
- 📅 Runs for a specified duration (10 days)
- 👥 Supports CC recipients
- 🔒 Secure credential management using environment variables
- 🚀 Auto-starts on Raspberry Pi boot
- 📝 Detailed logging for troubleshooting

## Prerequisites
- Raspberry Pi with Raspberry Pi OS installed
- Python 3.6 or higher
- Gmail account with 2-Step Verification enabled
- Internet connection

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/gmail-automation-pi
cd gmail-automation-pi
```

### 2. Install Required Packages
```bash
sudo apt update
sudo apt install python3-pip
pip3 install python-dotenv schedule
```

### 3. Set Up Gmail App Password
1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to Security > 2-Step Verification
3. Scroll down and select "App passwords"
4. Generate a new app password:
   - Select app: "Mail"
   - Select device: "Other (Custom name)" - Enter "Raspberry Pi"
   - Click "Generate"
5. Copy the 16-character password (will be used in the next step)

### 4. Configure Environment Variables
Create a `.env` file in the project directory:
```bash
nano .env
```

Add your configuration:
```
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=your16charpassword
RECIPIENT_EMAIL=primary.recipient@example.com
CC_RECIPIENTS=person1@example.com,person2@example.com
```

### 5. Test the Script
```bash
python3 email_sender.py
```

## Setting Up Auto-start on Boot

### 1. Create System Service
```bash
sudo nano /etc/systemd/system/email-automation.service
```

Add the following content:
```ini
[Unit]
Description=Email Automation Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/gmail-automation-pi/email_sender.py
WorkingDirectory=/home/pi/gmail-automation-pi
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start the Service
```bash
sudo systemctl enable email-automation
sudo systemctl start email-automation
```

## Monitoring and Management

### Check Service Status
```bash
sudo systemctl status email-automation
```

### View Logs
```bash
journalctl -u email-automation -f
```

### Control the Service
```bash
# Stop the service
sudo systemctl stop email-automation

# Start the service
sudo systemctl start email-automation

# Restart the service
sudo systemctl restart email-automation
```

## Troubleshooting

### Common Issues and Solutions

1. Authentication Error (535, 5.7.8):
   - Verify that your Gmail address is correct
   - Ensure 2-Step Verification is enabled
   - Generate a new App Password
   - Check for spaces or typos in the App Password

2. Connection Issues:
   - Check internet connectivity
   - Verify that port 587 is not blocked
   - Ensure the Raspberry Pi's date/time is correct

3. Service Not Starting:
   - Check file permissions
   - Verify Python path
   - Check system logs for errors

### Testing Credentials
Use the included `test_credentials.py` script to verify your setup:
```bash
python3 test_credentials.py
```

## Customization

### Modifying Email Schedule
To change the email frequency, modify the schedule line in `email_sender.py`:
```python
# Change from 6 hours to your desired interval
schedule.every(6).hours.do(sender.send_email)
```

### Modifying Email Content
Edit the `send_email` method in the `EmailSender` class to customize:
- Email subject
- Email body
- HTML formatting (if needed)

## Security Notes
- Keep your `.env` file secure and never commit it to version control
- Use App Password instead of your main Gmail password
- Regularly update your Raspberry Pi and Python packages
- Monitor the logs for any suspicious activity

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
- [schedule](https://github.com/dbader/schedule) for task scheduling
