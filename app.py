import time
import re
import ast
import operator as op
import streamlit as st

st.set_page_config(page_title="Chatbot Dummy - Streamlit", page_icon="💬")

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    mode = st.selectbox(
        "Mode balasan",
        [
            "Echo (ulang pesanmu)",
            "Uppercase (huruf besar)",
            "Reverse (dibalik)",
            "FAQ (regex)",
            "Kalkulator sederhana",
        ],
        index=0,
    )
    simulate_stream = st.checkbox("Simulasikan pengetikan (streaming)", value=True)
    chunk_size = st.slider("Kecepatan stream (huruf per chunk)", 1, 20, 5, 1, disabled=not simulate_stream)
    if st.button("🧹 Clear chat"):
        st.session_state.clear()
        st.rerun()
    st.markdown("---")
    st.caption("Ini versi *dummy* — tidak butuh API key. Cocok buat belajar UI/UX dulu.")

st.title("🤖 Chatbot Dummy (Streamlit)")

# --- Init State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a cheerful dummy bot that answers deterministically."}
    ]

# --- Helpers ---
def faq_answer(text: str) -> str:
    pairs = [
        (r"^hai|^halo|^hello", "Halo! Aku bot dummy. Cobain tanya apa pun 😄"),
        (r"siapa kamu|kamu siapa", "Aku chatbot dummy di Streamlit, buat latihan tanpa API."),
        (r"bisa apa", "Aku bisa echo, uppercase, reverse, FAQ sederhana, dan kalkulator aritmetika (+-*/^)."),
        (r"(jam|waktu) berapa", "Aku tidak cek jam sistem, tapi kamu bisa tanya hal lain ✨"),
        (r"siapa pembuatmu|dibuat oleh siapa", "Dibuat oleh kamu juga bisa—kode ada di file app.py 😉"),
    ]
    for pattern, ans in pairs:
        if re.search(pattern, text, flags=re.I):
            return ans
    return "Aku belum punya jawabannya. Coba mode lain, mis. Kalkulator: `2*(10+5)`."

# Safe eval for calculator
# Allowed operators
ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

def eval_expr(node):
    if isinstance(node, ast.Num):  # literal numbers (Py<3.8)
        return node.n
    if isinstance(node, ast.Constant):  # numbers (Py>=3.8)
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")
    if isinstance(node, ast.BinOp):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError(f"Operator not allowed: {op_type.__name__}")
        return ALLOWED_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = eval_expr(node.operand)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError(f"Operator not allowed: {op_type.__name__}")
        return ALLOWED_OPS[op_type](operand)
    raise ValueError("Invalid expression")

def safe_calc(expr: str) -> str:
    try:
        parsed = ast.parse(expr, mode="eval")
        result = eval_expr(parsed.body)
        return f"Hasil: {result}"
    except Exception as e:
        return f"Ekspresi tidak valid. Contoh: 2*(10+5) atau 5^2 (pakai **):\nError: {e}"

def generate_reply(user_text: str) -> str:
    if mode == "Echo (ulang pesanmu)":
        return f"Kamu bilang: {user_text}"
    elif mode == "Uppercase (huruf besar)":
        return user_text.upper()
    elif mode == "Reverse (dibalik)":
        return user_text[::-1]
    elif mode == "FAQ (regex)":
        return faq_answer(user_text)
    elif mode == "Kalkulator sederhana":
        # ganti caret menjadi ** agar familiar
        expr = user_text.replace("^", "**")
        return safe_calc(expr)
    else:
        return "Mode tidak dikenal."

def stream_text(text: str, chunk: int = 5):
    for i in range(0, len(text), chunk):
        yield text[i : i + chunk]
        time.sleep(0.03)

# --- Render history (skip system) ---
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

# --- Chat input ---
if prompt := st.chat_input("Tulis pesan kamu…"):
    # Show & store user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate reply
    reply = generate_reply(prompt)

    # Display assistant message (streaming optional)
    with st.chat_message("assistant"):
        if simulate_stream:
            full = st.write_stream(stream_text(reply, chunk_size))
        else:
            st.markdown(reply)
            full = reply

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": full})

# --- Footer ---
st.caption("💡 Tip: Ganti *Mode balasan* di sidebar untuk mencoba perilaku berbeda.")
