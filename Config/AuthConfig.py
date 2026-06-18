from passlib.context import CryptContext
# configuration for password hashing and verification using the passlib library.
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
    )

# Function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
        )

# Function to hash the password
def get_password_hash(password):
    return pwd_context.hash(password)