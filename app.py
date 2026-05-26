import streamlit as st
import random
from datetime import datetime
from fpdf import FPDF
import base64

# पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# लॉगिन सिस्टम
USER_DATA = {"admin": "12345"}
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.subheader("🔐 लॉगिन करें")
    username = st.text_input("यूजरनेम")
    password = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if username in USER_DATA and USER_DATA[username] == password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

# रसीद बनाना और PDF में बदलना
def create_pdf(rb):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="MAA PROPERTIES", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Invoice No: {rb['id']} | Date: {rb['date']}", ln=True)
    pdf.cell(200, 10, txt=f"Property: {rb['b_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Area: {rb['area']} SqFt", ln=True)
    pdf.cell(200, 10, txt=f"Location: {rb['loc']}", ln=True)
    pdf.cell(200, 10, txt=f"Buyer: {rb['c_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Mobile: {rb['c_phone']}", ln=True)
    pdf.cell(200, 10, txt=f"Total: {rb['base']} | Due: {rb['due']}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

tab1, tab2 = st.tabs(["💳 नई रसीद", "📜 हिस्ट्री"])

with tab1:
    b_name = st.text_input("प्रॉपर्टी का नाम")
    area = st.text_input("एरिया (SqFt)")
    loc = st.text_input("लोकेशन")
    c_name = st.text_input("खरीदार")
    c_phone = st.text_input("मोबाइल नंबर")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)
    
    if st.button("✨ रसीद जेनरेट करें"):
        bill_data = {
            "id": random.randint(1000, 9999), "b_name": b_name.upper(), "area": area, 
            "loc": loc.upper(), "c_name": c_name.upper(), "c_phone": c_phone, 
            "base": base, "due": base-adv, "date": datetime.now().strftime('%d-%m-%Y')
        }
        st.session_state.current_pdf = create_pdf(bill_data)
        st.session_state.bill_records = st.session_state.get('bill_records', []) + [bill_data]
        st.success("रसीद तैयार है!")

    if 'current_pdf' in st.session_state:
        st.download_button(
            label="📥 रसीद डाउनलोड करें (PDF)",
            data=st.session_state.current_pdf,
            file_name="receipt.pdf",
            mime="application/pdf"
        )

with tab2:
    st.subheader("📜 हिस्ट्री")
    if 'bill_records' in st.session_state:
        for r in reversed(st.session_state.bill_records):
            st.write(f"🆔 {r['id']} | 👤 {r['c_name']} | 🏢 {r['b_name']}")
