import logging
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('birthday_emailer.log'),
        logging.StreamHandler()
    ]
)

def check_birthdays():
    """Check CSV file for today's birthdays"""
    try:
        df = pd.read_csv('birthdays.csv')
        today = datetime.now().strftime('%m-%d')
        logging.info(f"Today's date (MM-DD): {today}")
        
        # Convert birthday column to same format as today (mm-dd)
        df['birthday'] = pd.to_datetime(df['birthday']).dt.strftime('%m-%d')
        logging.info("Converted birthdays in CSV:")
        for _, row in df.iterrows():
            logging.info(f"- {row['name']}: {row['birthday']}")
            
        matches = df[df['birthday'] == today]
        logging.info(f"Found {len(matches)} matches for today's date")
        return matches
    except Exception as e:
        logging.error(f"Error checking birthdays: {str(e)}")
        print(f"Error: {str(e)}")
        return pd.DataFrame()

def send_birthday_email(name, email):
    """Send birthday email to a person"""
    try:
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('EMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            logging.error("Missing email credentials in environment variables")
            return
            
        logging.info(f"Attempting to send email from {sender_email} to {email}")
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"Happy Birthday {name}!"
        
        body = f"""
        Dear {name},
        
        Happy Birthday! 🎉 🎂 
        Wishing you a fantastic day filled with joy and celebration!
        
        Best wishes,
        Your Automated Birthday Wisher
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        logging.info("Connecting to Gmail SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            logging.info("Attempting login...")
            server.login(sender_email, sender_password)
            logging.info("Sending email...")
            server.send_message(msg)
            
        logging.info(f"Successfully sent birthday email to {name}")
    except Exception as e:
        logging.error(f"Detailed error sending email to {name}: {str(e)}")
        # Print the type of error
        logging.error(f"Error type: {type(e).__name__}")

def main():
    """Main function to check and send birthday emails"""
    logging.info("Checking for birthdays...")
    birthday_people = check_birthdays()
    
    if len(birthday_people) > 0:
        logging.info(f"Found {len(birthday_people)} birthdays today:")
        for _, person in birthday_people.iterrows():
            logging.info(f"- {person['name']} ({person['email']})")
            send_birthday_email(person['name'], person['email'])
        logging.info(f"Sent {len(birthday_people)} birthday emails")
    else:
        logging.info("No birthdays today")

if __name__ == "__main__":
    main() 