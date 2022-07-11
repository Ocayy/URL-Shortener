import hashlib
import base64

def generate_short_url( redirect_url: str,
                        timestamp: str
                        ) -> str:
    string_to_encode = f"{redirect_url}{timestamp.replace(' ', '')}"

    encoded_string = base64.urlsafe_b64encode(
        hashlib.sha256(
            string_to_encode.encode()
        ).digest()
    ).decode()

    return encoded_string[:7]
