import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from dotenv import load_dotenv

# Replace the email configuration section with:
load_dotenv()  # Load environment variables

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

def read_birthdays():
    """Read the birthdays CSV file"""
    try:
        # Explicitly specify the expected columns
        df = pd.read_csv('birthdays.csv', 
                        encoding='utf-8',
                        names=['name', 'email', 'birthday'],
                        header=0)  # Use first row as header
        
        # Convert birthday strings to datetime, handling multiple formats
        df['birthday'] = pd.to_datetime(df['birthday'], format='mixed')
        
        print("Successfully loaded birthdays:")
        print(df)  # This will help us debug the data loading
        
        return df
    except Exception as e:
        print(f"Error reading birthdays file: {str(e)}")
        raise

def check_birthdays():
    """Check if anyone has a birthday today"""
    df = read_birthdays()
    today = datetime.datetime.now().date()
    print(f"Today's date: {today}")  # Debug print
    
    birthday_people = df[
        (df['birthday'].dt.month == today.month) & 
        (df['birthday'].dt.day == today.day)
    ]
    
    print(f"Found {len(birthday_people)} birthdays today")  # Debug print
    if len(birthday_people) > 0:
        print("Birthday people today:", birthday_people[['name', 'email', 'birthday']])
    
    return birthday_people

def send_birthday_email(name, email):
    """Send birthday email to a person"""
    # Create email content
    subject = f"Happy Birthday {name}! 🎉"
    body = f"""
    Dear {name},

    Wishing you a very happy birthday! 🎂
    May your day be filled with joy and celebration!

    Best wishes,
    [Vamsi Yarramreddy]
    """

    # Setup email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email
        server.send_message(msg)
        print(f"Birthday email sent to {name}")
        
        server.quit()
    except Exception as e:
        print(f"Error sending email to {name}: {str(e)}")

def main():
    """Main function to check and send birthday emails"""
    print("Checking for birthdays...")
    birthday_people = check_birthdays()
    
    if len(birthday_people) > 0:
        print(f"Found {len(birthday_people)} birthdays today:")
        for _, person in birthday_people.iterrows():
            print(f"- {person['name']} ({person['email']})")
            send_birthday_email(person['name'], person['email'])
        print(f"Sent {len(birthday_people)} birthday emails")
    else:
        print("No birthdays today")

def test_email(test_email):
    """Test function to send a test email"""
    print(f"Sending test email to {test_email}...")
    try:
        send_birthday_email("Test Person", test_email)
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error in test email: {str(e)}")

if __name__ == "__main__":
    # Comment out the test line and uncomment main()
    # test_email("vamsi.s.yarramreddy@gmail.com")  # This was sending test emails regardless of date
    main()  # This will check for today's birthdays 