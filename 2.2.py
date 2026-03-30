from Crypto.Cipher import AES # pyright: ignore[reportMissingImports]
key = b'1234567890123456'
plaintext = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_" # 32 bytes (2 blocks)
# 1. AES-ECB
cipher_ecb = AES.new(key, AES.MODE_ECB)
ct_ecb = cipher_ecb.encrypt(plaintext)
# 2. AES-CBC
cipher_cbc = AES.new(key,AES.MODE_CBC)
ct_cbc = cipher_cbc.encrypt(plaintext)
print(f"ECB: {ct_ecb.hex()}")
print(f"CBC: {ct_cbc.hex()}")