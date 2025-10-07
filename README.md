# Hollow Knight: Silksong Save Decoder

> A lightweight Streamlit web app to decrypt and visualize your **Hollow Knight: Silksong** save files (`user1.dat`) into human-readable JSON format.

---

##  Overview

This tool lets you **upload your Silksong `.dat` save file**, decrypt it using the known AES key and header pattern, and **view or export** it as a structured `.json` file.

Perfect for:
- Backup & inspection of save progress  
- Debugging or research on Silksong’s save structure  
- Data visualization for fan tools or mod development  

---

## 🧰 Requirements

| Dependency | Version |
|-------------|----------|
| Python | 3.10+ |
| Streamlit | 1.50.0 |
| PyCryptodome | 3.23.0 |

Or just install directly:

```bash
py -m pip install -r requirements.txt
````

**`requirements.txt`:**

```txt
streamlit==1.50.0
pycryptodome==3.23.0
```

---

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/silksong-save-decoder.git
   cd silksong-save-decoder
   ```

2. Install dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```


4. Open your browser (default: `http://localhost:8501`) and upload your Silksong save file:

   - **Windows:**  
     `C:/Users/<username>/AppData/LocalLow/Team Cherry/Hollow Knight Silksong/default/user1.dat`

5. View and export the decoded save as `silksong_save.json`.

---

## 🧩 File Structure

```
silksong-save-decoder/
├── app.py
├── requirements.txt
├── silksong_save.json      ← (output)
└── README.md
```

---

## Technical Details

### How it works

1. **Removes the Unity header**
2. **Decodes Base64 chunks**
3. **Decrypts the AES payload**
4. **Parses the resulting UTF-8 JSON**

---

## Disclaimer

This project is **for educational and personal use only.**
Do **not** use it to tamper with or redistribute proprietary data.
All rights for *Hollow Knight: Silksong* belong to **Team Cherry**.
---

## Credits

* Original AES decoding logic inspired by [th3r3dfox/silksong-tracker](https://github.com/th3r3dfox/silksong-tracker)
---


---

## Screenshots

<img src="https://user-images.githubusercontent.com/your-screenshot.png" width="600" alt="UI Screenshot"/>

---

Would you like me to include a section for the **reverse script (JSON → DAT re-encryptor)** too, so it’s ready when that part works cleanly?
