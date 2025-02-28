import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('birthday_emailer.log'),
        logging.StreamHandler()
    ]
)

# Replace print statements with logging
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