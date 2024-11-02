from library import *

# Hash a password using MD5
def hash_password(password):
    # Encode the password to bytes, then hash with MD5
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password

def get_time_now_ms():
    # Get the current time in milliseconds
    current_time_ms = int(time.time() * 1000)
    return current_time_ms


def initialize_counter(sequence_name):
    """
    Initialize the counter if it does not exist. Sets the starting sequence value to 0.
    """
    if not counter_collection.find_one({"_id": sequence_name}):
        counter_collection.insert_one({"_id": sequence_name, "sequence_value": 0})

def get_next_sequence_value(sequence_name):
    """
    Get the next sequential ID by incrementing the counter for a specific sequence name.
    """
    # Ensure the counter is initialized
    initialize_counter(sequence_name)

    # Find the counter and increment it atomically
    result = counter_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return result["sequence_value"]

def generate_session_id():
    # Generate a 32-character hex string as a unique session ID
    return secrets.token_hex(16)  # 16 bytes = 32 hex characters