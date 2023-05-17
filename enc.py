from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
key = Fernet.generate_key()
print(key)

# Create a Fernet object with the key
fernet = Fernet(key)

# Define a password to be encrypted
password = "sI6HeF&P!$BrLsTi?udL".encode()

# Encrypt the password
encrypted_password = fernet.encrypt(password)
# Print the encrypted password
print(encrypted_password)

# Decrypt the password
decrypted_password = fernet.decrypt(encrypted_password)

# Print the decrypted password
print(decrypted_password)

