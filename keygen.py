import os
import string
from random import SystemRandom

charset = string.ascii_letters + string.digits + string.punctuation

secret_key = ''.join(SystemRandom().choice(charset) for _ in range(50))

os.makedirs('signature', exist_ok = True)
key_file = 'signature/secret_key.txt'

if not os.path.exists(key_file):
    with open(key_file, 'w') as f:
        f.write(secret_key)
    print(f"\nSecret key geenrated and saved to {key_file}.\n")
else:
    print(f"\nSecret key file already exists at {key_file}.\n")