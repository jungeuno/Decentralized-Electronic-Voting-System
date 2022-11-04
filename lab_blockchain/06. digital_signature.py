from ecdsa import SigningKey
import hashlib

private_key = SigningKey.generate()
public_key = private_key.get_verifying_key()
wallet_address = hashlib.sha256(public_key.to_string()).hexdigest()

data = 'data'

signature = private_key.sign(data.encode())
print(signature)

try:
    public_key.verify(signature, data.encode())
    print('일치')
except:
    print('불일치')

try:
    public_key.verify('modified_data'.encode(), data.encode())
    print('일치')
except:
    print('불일치')