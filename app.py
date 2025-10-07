import streamlit as st
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import io

# --- Constants from Silksong tracker ---
CSHARP_HEADER = bytes([
    0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0
])

AES_KEY_STRING = "UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"

def sanitize_key(key_str: str) -> bytes:
    """Ensure AES key is valid (16/24/32 bytes)."""
    key_bytes = key_str.strip().encode("utf-8")
    if len(key_bytes) not in (16, 24, 32):
        # pad or trim to 32 bytes for AES-256
        if len(key_bytes) > 32:
            key_bytes = key_bytes[:32]
        else:
            key_bytes = key_bytes.ljust(32, b"\0")
    return key_bytes

def remove_header(data: bytes) -> bytes:
    """Remove Unity/C# header and length prefix."""
    without_header = data[len(CSHARP_HEADER):-1]
    length_count = 0
    for i in range(5):
        length_count += 1
        if (without_header[i] & 0x80) == 0:
            break
    return without_header[length_count:]

def decode_silksong_save(data: bytes):
    """Decode Silksong .dat -> JSON or binary text."""
    try:
        no_header = remove_header(data)

        b64_chunks = []
        chunk_size = 0x8000
        for i in range(0, len(no_header), chunk_size):
            b64_chunks.append(no_header[i:i + chunk_size].decode("latin1"))
        b64_string = "".join(b64_chunks)

        # Decode base64
        encrypted = base64.b64decode(b64_string)

        # AES decrypt (ECB / PKCS7)
        key = sanitize_key(AES_KEY_STRING)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted)

        try:
            decrypted = unpad(decrypted, AES.block_size)
        except ValueError:
            pass  

        try:
            json_str = decrypted.decode("utf-8")
            if json_str.strip().startswith("{"):
                return json.loads(json_str)
            else:
                raise ValueError("Decryption OK but not JSON")
        except Exception:
            # fallback: show readable binary text
            return {"raw_text": decrypted[:500].decode("latin1", errors="ignore")}
    except Exception as e:
        raise ValueError(f"Failed to decode Silksong save: {e}")


st.set_page_config(page_title="Silksong Save Decoder", page_icon="🕸️")
st.title("Hollow Knight: Silksong Save Decoder")

uploaded_file = st.file_uploader("Upload your Silksong save (.dat)", type=["dat"])

if uploaded_file:
    try:
        file_bytes = uploaded_file.read()
        decoded_data = decode_silksong_save(file_bytes)

        st.success("Successfully decoded Silksong save!")
        st.json(decoded_data)

        if isinstance(decoded_data, dict):
            json_data = json.dumps(decoded_data, indent=2)
            st.download_button(
                "Download JSON",
                data=json_data.encode("utf-8"),
                file_name="silksong_save.json",
                mime="application/json"
            )
    except Exception as e:
        st.error(str(e))
else:
    st.info("Upload a `.dat` file to decode it.")