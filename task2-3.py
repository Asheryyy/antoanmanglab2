from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

def count_diff_bits(b1: bytes, b2: bytes) -> int:
    x = int.from_bytes(b1, 'big') ^ int.from_bytes(b2, 'big')
    return bin(x).count('1')

def avalanche_test(key):
    key = b'24521538'   # 8 byte
    p1 = b'STAYHOME'
    p2 = b'STAYHOMF'    # khác 1 ký tự cuối so với p1

    cipher1 = DES.new(key, DES.MODE_ECB)
    cipher2 = DES.new(key, DES.MODE_ECB)

    encrypted1 = cipher1.encrypt(pad(p1, 8))
    encrypted2 = cipher2.encrypt(pad(p2, 8))

    print("Ciphertext 1:", encrypted1)
    print("Ciphertext 2:", encrypted2)

    bit1= bin(int.from_bytes(encrypted1, 'big'))
    bit2= bin(int.from_bytes(encrypted2, 'big'))

    print("Chuoi bit cua ciphertext1: ", bit1)
    print("Chuoi bit cua ciphertext2: ", bit2)


    bits_diff = count_diff_bits(encrypted1, encrypted2)
    total_bits = len(encrypted1) * 8
    percent = bits_diff / total_bits * 100

    print("Số bit khác nhau:", bits_diff)
    print("Tỷ lệ thay đổi:", f"{percent:.2f}%")

    return encrypted1, encrypted2, bits_diff, percent
key= input("Nhap key(MSSV): ")
avalanche_test(key)