import streamlit as st
import random
from datetime import datetime

# पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# प्रिंट के लिए एकदम सटीक CSS
st.markdown("""
<style>
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { 
            position: absolute; left: 0; top: 0; width: 100%; 
            border: 2px solid #000; padding: 20px;
        }
    }
    .receipt-box { border: 2px solid #000; padding: 20px; max-width: 400px; margin: auto; }
</style>
""", unsafe_allow_html=True)

# लॉगिन सिस्टम
USER_DATA = {"admin": "12345"}
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("यूजरनेम")
    password = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if username in USER_DATA and USER_DATA[username] == password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# बिलिंग फॉर्म
st.title("⚡ मां प्रॉपर्टी 2026")
b_name = st.text_input("प्रॉपर्टी का नाम")
area = st.text_input("एरिया (SqFt)")
loc = st.text_input("लोकेशन")
c_name = st.text_input("खरीदार")
c_phone = st.text_input("मोबाइल नंबर")
base = st.number_input("कुल राशि", value=0)
adv = st.number_input("एडवांस", value=0)

if st.button("रसीद तैयार करें"):
    st.session_state.current_bill = {
        "id": random.randint(1000, 9999), "b_name": b_name, "area": area, 
        "loc": loc, "c_name": c_name, "c_phone": c_phone, 
        "base": base, "due": base - adv
    }

# रसीद का हिस्सा (जो प्रिंट होगा)
if 'current_bill' in st.session_state:
    rb = st.session_state.current_bill
    st.markdown(f"""
    <div class="printable-area receipt-box">
        <h2 style="text-align:center;">MAA PROPERTIES</h2>
        <p><b>Inv:</b> {rb['id']} | <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}</p>
        <hr>
        <p><b>Property:</b> {rb['b_name']}</p>
        <p><b>Area:</b> {rb['area']} SqFt</p>
        <p><b>Location:</b> {rb['loc']}</p>
        <p><b>Buyer:</b> {rb['c_name']}</p>
        <p><b>Mobile:</b> {rb['c_phone']}</p>
        <p><b>Total:</b> ₹{rb['base']:,} | <b>Due:</b> ₹{rb['due']:,}</p>
        <br><br>
        <div style="display:flex; justify-content: space-between;">
            <span>_______<br>Buyer</span><span>_______<br>Seller</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.warning("🖨️ अब कीबोर्ड से Ctrl + P दबाएं। सिर्फ रसीद प्रिंट होगी।")
