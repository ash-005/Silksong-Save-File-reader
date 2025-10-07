import streamlit as st
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import io
from PIL import Image

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



# --- UI Improvements ---
st.set_page_config(
    page_title="Silksong Save Decoder",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar with instructions and credits
with st.sidebar:
    st.markdown("""
    ## Silksong Save Decoder
    
    **How to use:**
    1. Click **Browse files** below and select your `user1.dat` save file.
    2. Wait for the file to decode (success message will appear).
    3. View your save as JSON, and download it if you wish.
    
    **File location:**
    - Windows:  
      `C:/Users/&lt;username&gt;/AppData/LocalLow/Team Cherry/Hollow Knight Silksong/default/user1.dat`
    
    ---
    [GitHub Repo](https://github.com/ash-005/Silksong-Save-File-reader)
    """)
    st.caption("""Made with ❤️ for the Silksong community.  
    Not affiliated with Team Cherry.
    """)

# Main UI
st.markdown("""
<h1 style='text-align: center; color: #f3260fff; font-family: monospace;'>
  🕸️ Hollow Knight: Silksong Save Decoder
</h1>
<p style='text-align: center; color: #aaa; font-size: 1.1em;'>
  Decrypt and view your Silksong save file as readable JSON.<br>
  <span style='color:#f3260fff;'>No data leaves your device.</span>
</p>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div style='background-color: #1a1a1a; border-radius: 8px; padding: 1.2em 1em; margin-bottom: 1.5em;'>
<b>Step 1:</b> <span style='color:#f3260fff;'>Upload your <code>user1.dat</code> save file</span> below.<br>
<b>Step 2:</b> Wait for the decoder to process your file.<br>
<b>Step 3:</b> View and download your save as JSON.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["dat"],
    label_visibility="collapsed",
    help="Upload your Silksong save file (user1.dat)"
)

if uploaded_file:
    with st.spinner("Decoding your save file..."):
        try:
            file_bytes = uploaded_file.read()
            decoded_data = decode_silksong_save(file_bytes)
            
            st.success("Successfully decoded your Silksong save!")
            if isinstance(decoded_data, dict):
                json_data = json.dumps(decoded_data, indent=2)
                st.download_button(
                    "⬇️ Download as JSON",
                    data=json_data.encode("utf-8"),
                    file_name="silksong_save.json",
                    mime="application/json",
                    help="Download your decoded save as a JSON file."
                )
            st.markdown("<b>Preview:</b>", unsafe_allow_html=True)
            st.json(decoded_data)

            
        except Exception as e:
            st.error(f"❌ {str(e)}")
else:
    st.info("<b>Waiting for file upload...</b> <br>Click above to select your <code>user1.dat</code> save file.", icon="📂")