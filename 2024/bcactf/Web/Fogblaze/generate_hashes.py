import hashlib
import itertools
import json

# Define the set of characters and the exact length of combinations
chrs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
length = 4

# File to save the generated hashes
hashes_file = "generated_hashes.json"

def compute_md5(s):
    """Compute the MD5 hash of a given string."""
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def generate_hashes(chrs, length):
    """Generate all possible combinations of the characters of the exact length and compute their MD5 hashes."""
    hashes = {}
    for word in itertools.product(chrs, repeat=length):
        word_str = ''.join(word)
        md5_hash = compute_md5(word_str)
        hashes[md5_hash] = word_str
    
    with open(hashes_file, 'w') as f:
        json.dump(hashes, f, indent=4)

if __name__ == "__main__":
    generate_hashes(chrs, length)
    print(f"All possible hashes generated and saved to {hashes_file}")
