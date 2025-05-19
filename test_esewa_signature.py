import hmac
import hashlib
import base64

def generate_signature(message, secret):
    hmac_sha256 = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    )
    digest = hmac_sha256.digest()
    return base64.b64encode(digest).decode('utf-8')

# Test case from eSewa documentation
test_message = "100,11-201-13,EPAYTEST"
test_secret = "8gBm/:&EnhH.1/q"
test_signature = generate_signature(test_message, test_secret)

print("Test case from documentation:")
print(f"Message: {test_message}")
print(f"Secret: {test_secret}")
print(f"Generated signature: {test_signature}")

# Our actual message from debug output
actual_message = "499,250506-150458,EPAYTEST"
actual_secret = "8gBm/:&EnhH.1/q"
actual_signature = generate_signature(actual_message, actual_secret)

print("\nOur actual message:")
print(f"Message: {actual_message}")
print(f"Secret: {actual_secret}")
print(f"Generated signature: {actual_signature}")

# Try with different formats
test_cases = [
    ("100,11-201-13,EPAYTEST", "Documentation example"),
    ("499,250506-150458,EPAYTEST", "Our current format"),
    ("499.0,250506-150458,EPAYTEST", "With decimal"),
    ("499,250506-150458,EPAYTEST", "Original format"),
]

print("\nTesting different formats:")
for msg, desc in test_cases:
    sig = generate_signature(msg, test_secret)
    print(f"\n{desc}:")
    print(f"Message: {msg}")
    print(f"Signature: {sig}")
    
    # Compare with documentation example
    if msg == test_message:
        print("✓ Matches documentation example")
    else:
        print("✗ Different from documentation example") 