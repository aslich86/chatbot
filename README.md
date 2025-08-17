# Streamlit Dummy Chatbot (No API Key)

Chatbot *dummy* untuk latihan UI/UX **Streamlit** tanpa butuh API key. Menyediakan beberapa mode balasan:
- Echo
- Uppercase
- Reverse
- FAQ (regex)
- Kalkulator sederhana (+, -, *, /, **, %, //)

## 1) Setup Lokal
```bash
cd streamlit-dummy-chatbot
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 2) Deploy ke Streamlit Community Cloud
1. Push project ini ke GitHub.
2. Buka Streamlit Community Cloud → **Create app** → pilih repo & branch.
3. Deploy. (Tidak perlu Secrets karena tidak ada API key.)

## 3) Kustomisasi
- Tambah mode balasan di fungsi `generate_reply`.
- Ubah daftar FAQ di `faq_answer`.
- Atur kecepatan *streaming* di sidebar.

---
> Setelah nyaman, kamu bisa upgrade ke versi pakai API (OpenAI/Ollama/prov lain) dengan mengganti fungsi `generate_reply` untuk memanggil model.
