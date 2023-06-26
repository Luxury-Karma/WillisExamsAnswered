import json
import os
import base64
from typing import Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# region Key handling


def generate_base_key_and_salt() -> tuple[bytes, bytes]:
    """
    Generate the key and salt
    :return: The key and the salt
    """
    base_key = Fernet.generate_key()
    base_salt = os.urandom(16)
    return base_key, base_salt


def derive_key(base_key, base_salt, password, iterations=100000) -> bytes:
    """
    Generate the real encryption key
    :param base_key: The original key
    :param base_salt: the salt
    :param password: the file password
    :param iterations: The amount of iteration
    :return: The derived key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base_salt,
        iterations=iterations,
        backend=default_backend()
    )
    derived_key = kdf.derive(b''.join([base_key, bytes(password.encode('UTF-8'))]))
    derived_key_base64 = base64.urlsafe_b64encode(derived_key)
    return derived_key_base64


def encrypt_file(filename, password, base_key, base_salt) -> None:
    """
    Encrypt the profile file with password, key, salt
    :param filename: The file of the user
    :param password: password for the file
    :param base_key: the key for the file
    :param base_salt: the salt for the file
    :return: None
    """
    cipher = Fernet(derive_key(base_key, base_salt, password))

    with open(filename, 'rb') as file:
        file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(base_salt + encrypted_data)

    print(f"File '{filename}' encrypted successfully. Encrypted file: '{filename}'")


def decrypt_data(encrypted_data, password, base_key, base_salt) -> bytes:
    """
    Decrypt the user file data
    :param encrypted_data: The encrypted data
    :param password: The file's password
    :param base_key:  The file's key
    :param base_salt: The file's password
    :return: Decrypted data
    """
    cipher = Fernet(derive_key(base_key, base_salt, password))

    encrypted_data = encrypted_data[16:]  # Extract the encrypted data from the file

    decrypted_data = cipher.decrypt(encrypted_data)

    return decrypted_data


def create_data_file(path_to_data, username: str, password: str, file_password: str, key_path) -> None:
    """
    Create the files for handling connections with willis college's website
    :param path_to_data: The path for the json file
    :param username: The willis email
    :param password: The email's password
    :param file_password: the file's password
    :param key_path: the path to the key file
    :return: None
    """
    data = willis_account_creation(username, password)
    # Create the file initially
    if not os.path.isdir('userFile'):
        os.mkdir('userFile')
    with open(path_to_data, 'w') as f:
        json.dump(data, f)
        f.flush()
    base_key, base_salt = generate_base_key_and_salt()
    save_key_and_salt_to_file(base_key, base_salt, key_path)
    encrypt_file(path_to_data, file_password, base_key, base_salt)

# endregion


# region save to file

def save_key_and_salt_to_file(key, salt, file_name: str) -> None:
    """
    Save the key and the salt to a file
    :param key: The key
    :param salt: The salt
    :param file_name: The name of the file to save
    :return: None
    """
    key_encoded = base64.urlsafe_b64encode(key).decode('utf-8')
    salt_encoded = base64.urlsafe_b64encode(salt).decode('utf-8')
    with open(file_name, 'w') as file:
        file.write(key_encoded)
        file.write('\n')  # Add a newline to separate key and salt
        file.write(salt_encoded)


def willis_account_creation(username: str, password: str) -> dict:
    """
    Create the format for Willis accounts
    :param username: Willis email
    :param password: Willis email's password
    :return: The dictionary formatted correctly
    """
    return {'Willis_College_user': {'username': username, 'password': password}}


def data_detection(path_to_create):
    """
    Ensure that the file with the user data exists
    :return: if the file exists
    """
    return os.path.isfile(path_to_create)

# endregion


# region load


def load_key_and_salt_from_file(file_name: str) -> tuple[bytes, bytes]:
    """
    Load the key and the salt from the specified file
    :param file_name: The name of the file
    :return: The key and the salt loaded from the file
    """
    with open(file_name, 'r') as file:
        key_encoded = file.readline().strip()
        salt_encoded = file.readline().strip()
    key = base64.urlsafe_b64decode(key_encoded)
    salt = base64.urlsafe_b64decode(salt_encoded)
    return key, salt

# endregion
