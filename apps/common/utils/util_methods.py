import string
import secrets

def generate_random_alphanumeric_string(length=8):
    "default lenght set to 8"
    alphabet = string.ascii_letters + string.digits
    random_str = ''.join(secrets.choice(alphabet) for i in range(length))
    print("sandom string : ", random_str)
    return random_str

