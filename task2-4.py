from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16  # AES block size = 16 bytes


def flip_one_bit(data: bytes, index: int, bit_position: int = 0) -> bytes:

    arr = bytearray(data)
    arr[index] ^= (1 << bit_position)
    return bytes(arr)


def count_byte_differences(a: bytes, b: bytes) -> int:
    return sum(x != y for x, y in zip(a, b))


def show_error_propagation(mode_name: str, plaintext: bytes):
    key = get_random_bytes(16)   # AES-128
    iv = get_random_bytes(16)

    # Mã hóa
    if mode_name == "ECB":
        cipher_enc = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher_enc.encrypt(pad(plaintext, BLOCK_SIZE))

        # Làm hỏng bản mã: đảo 1 bit ở byte thứ 26
        corrupted_ciphertext = flip_one_bit(ciphertext, 25, 0)

        # Giải mã
        cipher_dec = AES.new(key, AES.MODE_ECB)
        decrypted = unpad(cipher_dec.decrypt(corrupted_ciphertext), BLOCK_SIZE)

    elif mode_name == "CBC":
        cipher_enc = AES.new(key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher_enc.encrypt(pad(plaintext, BLOCK_SIZE))

        corrupted_ciphertext = flip_one_bit(ciphertext, 25, 0)

        cipher_dec = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher_dec.decrypt(corrupted_ciphertext), BLOCK_SIZE)

    elif mode_name == "CFB":
        cipher_enc = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
        ciphertext = cipher_enc.encrypt(plaintext)

        corrupted_ciphertext = flip_one_bit(ciphertext, 25, 0)

        cipher_dec = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
        decrypted = cipher_dec.decrypt(corrupted_ciphertext)

    elif mode_name == "OFB":
        cipher_enc = AES.new(key, AES.MODE_OFB, iv=iv)
        ciphertext = cipher_enc.encrypt(plaintext)

        corrupted_ciphertext = flip_one_bit(ciphertext, 25, 0)

        cipher_dec = AES.new(key, AES.MODE_OFB, iv=iv)
        decrypted = cipher_dec.decrypt(corrupted_ciphertext)

    else:
        raise ValueError("Unsupported mode")

    diff_count = count_byte_differences(plaintext, decrypted)

    print(f"Mode: {mode_name}")
    print(f"Original plaintext length : {len(plaintext)}")
    print(f"Ciphertext length         : {len(ciphertext)}")
    print(f"Bytes different after decryption: {diff_count}")
    print(f"First 64 bytes plaintext : {plaintext[:64]}")
    print(f"First 64 bytes decrypted : {decrypted[:64]}")
    print("-" * 60)


def main():
    # Tạo 1000 byte dữ liệu
    plaintext = bytes([i % 256 for i in range(1000)])

    # Thử các chế độ
    for mode in ["ECB", "CBC", "CFB", "OFB"]:
        show_error_propagation(mode, plaintext)


if __name__ == "__main__":
    main()