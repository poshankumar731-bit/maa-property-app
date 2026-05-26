import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Maa Property 2026", layout="centered")

# CSS: बिल के स्वरूप को साफ़ और सुंदर बनाने के लिए
st.markdown("""
<style>
    .print-container { 
        width: 100%; max-width: 450px; border: 3px solid #000; 
        padding: 25px; margin: auto; font-family: 'Arial', sans-serif;
        background-color: white; color: black;
    }
    .header { text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 5px; }
    .sub-header { text-align: center; font-size: 18px; margin-bottom: 15px; }
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# लॉगिन सिस्टम
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    u = st.text_input("यूजर आईडी")
    p = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if u == "admin" and p == "12345": st.session_state.logged_in = True; st.rerun()
    st.stop()

st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

# डेटा मैनेजमेंट
if 'bills' not in st.session_state: st.session_state.bills = []

t1, t2 = st.tabs(["➕ नई रसीद", "📜 हिस्ट्री"])

with t1:
    b_name = st.text_input("प्रॉपर्टी का नाम")
    c_name = st.text_input("खरीदार का नाम")
    c_phone = st.text_input("खरीदार का मोबाइल नंबर")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)
    
    if st.button("रसीद तैयार करें"):
        new_bill = {
            "id": random.randint(1000,9999), "b_name": b_name.upper(), 
            "c_name": c_name.upper(), "c_phone": c_phone, 
            "base": base, "due": base - adv, 
            "date": datetime.now().strftime('%d-%m-%Y')
        }
        st.session_state.bills.append(new_bill)
        st.session_state.active_bill = new_bill
        st.success("रसीद तैयार है!")

# बिल का स्वरूप (जो प्रिंट होगा)
if 'active_bill' in st.session_state:
    rb = st.session_state.active_bill
    st.markdown(f"""
    <div class="printable-area print-container">
        <div class="header">MAA PROPERTIES MUNGELI</div>
        <div class="sub-header">Contact: +91 8109471091</div>
        <hr>
        <p><b>Invoice No:</b> {rb['id']} | <b>Date:</b> {rb['date']}</p>
        <p><b>Property:</b> {rb['b_name']}</p>
        <p><b>Buyer:</b> {rb['c_name']}</p>
        <p><b>Buyer Mobile:</b> {rb['c_phone']}</p>
        <p><b>Total Amount:</b> ₹{rb['base']:,}</p>
        <p><b>Balance Due:</b> ₹{rb['due']:,}</p>
        <br><br>
        <div style="display:flex; justify-content: space-between; margin-top: 40px;">
            <div>_______<br>Buyer Signature</div>
            <div>_______<br>Seller Signature</div>
        </div>
        <br>
        <div style="text-align:center; font-weight:bold; margin-top:20px;">
            Proprietor: VISHAL GUPTA
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("🖨️ प्रिंट करने के लिए अपने कीबोर्ड पर Ctrl + P दबाएं।")

with t2:
    for i, b in enumerate(st.session_state.bills):
        st.write(f"🆔 {b['id']} | 👤 {b['c_name']} | 🏢 {b['b_name']}")
