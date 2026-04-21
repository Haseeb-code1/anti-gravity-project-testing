import secrets
import string
import math

# Characters often confused by users
AMBIGUOUS_CHARS = "lI1O0"

def generate_password(length: int, use_upper: bool, use_lower: bool, use_digits: bool, use_special: bool, exclude_ambiguous: bool) -> str:
    """Generates a secure random password based on user constraints."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_special:
        pool += string.punctuation
        
    if not pool:
        raise ValueError("Please select at least one character type.")
        
    if exclude_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)
        
    if not pool:
        raise ValueError("Character pool is empty after excluding ambiguous characters.")
        
    # Use secrets for cryptographically strong random choice
    return "".join(secrets.choice(pool) for _ in range(length))

def calculate_entropy(password: str) -> float:
    """Calculates the entropy (in bits) of the generated password."""
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password): pool_size += 26
    if any(c in string.ascii_uppercase for c in password): pool_size += 26
    if any(c in string.digits for c in password): pool_size += 10
    if any(c in string.punctuation for c in password): pool_size += len(string.punctuation)
    
    if pool_size == 0:
        return 0.0
        
    entropy = len(password) * math.log2(pool_size)
    return entropy

def evaluate_strength(entropy: float) -> str:
    """Evaluates password strength based on entropy."""
    if entropy < 50:
        return "Weak"
    elif entropy < 80:
        return "Medium"
    else:
        return "Strong"
