from string import ascii_lowercase, ascii_uppercase, digits
import random


def create_user_password(pass_length=8, restricted_characters=None):
    special_characters = '!@#$%^&*()<=>-'
    all_characters = ascii_uppercase + ascii_lowercase + digits + special_characters
    if restricted_characters:
        all_characters = [
            char for char in all_characters if char not in restricted_characters
        ]
    while True:
        password = ''.join([random.choice(all_characters) for char in range(pass_length)])
        has_upper = any(char for char in password if char in ascii_uppercase)
        has_lower = any(char for char in password if char in ascii_lowercase)
        has_digit = any(char for char in password if char in digits)
        has_special = any(char for char in password if char in special_characters)
        if all([has_upper, has_lower, has_digit, has_special]):
            break
    return password
