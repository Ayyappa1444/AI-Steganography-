from PIL import Image
import hashlib


DELIMITER = "###END###"


def _derive_key(key: str) -> int:
    return sum(bytearray(key.encode())) % 256


def hide_message(image_path, message, key, output_path):
    img = Image.open(image_path).convert("RGB")
    data = list(img.getdata())

    key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    payload = f"{key_hash}:{message}{DELIMITER}"

    binary = ''.join(format(ord(c), '08b') for c in payload)

    if len(binary) > len(data) * 3:
        raise ValueError("Message too large for image")

    new_pixels = []
    idx = 0

    for r, g, b in data:
        if idx < len(binary):
            r = (r & 254) | int(binary[idx]); idx += 1
        if idx < len(binary):
            g = (g & 254) | int(binary[idx]); idx += 1
        if idx < len(binary):
            b = (b & 254) | int(binary[idx]); idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)


def extract_message(image_path, key):
    img = Image.open(image_path).convert("RGB")
    data = list(img.getdata())

    bits = ""
    for r, g, b in data:
        bits += str(r & 1) + str(g & 1) + str(b & 1)

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))

    extracted = "".join(chars)

    if DELIMITER not in extracted:
        raise ValueError("No hidden data found")

    extracted = extracted.split(DELIMITER)[0]

    try:
        stored_hash, message = extracted.split(":", 1)
    except ValueError:
        raise ValueError("Corrupted data")

    key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]

    if stored_hash != key_hash:
        raise ValueError("Wrong secret key")

    return message
