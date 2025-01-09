import base64

def decode_base64(content: str) -> str:
    """Decodes a base64 encoded string to a UTF-8 string."""
    try:
        decoded_bytes = base64.b64decode(content)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
       raise ValueError(f"Error during base64 decoding: {e}")