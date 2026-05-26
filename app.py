import streamlit as st
import random
from datetime import datetime

# पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# प्रिंट के लिए एकदम सटीक CSS (यह बिल को एक पेज पर रखेगा)
st.markdown("""
<style>
    .print-container { 
        width: 100%; max-width: 400px; margin: auto; 
        border: 2px solid #000; padding: 20px; font-family: Arial, sans-serif;
    }
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
        @page { size: A4 portrait; margin: 10mm; }
    }
</style>
""", unsafe_allow_html=True)

# लॉगिन सिस्टम
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.subheader("🔐 लॉगिन करें")
    if st.text_input("पासवर्ड", type="password") == "12345":
        if st.button("लॉगिन"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

# इनपुट फॉर्म
b_name = st.text_input("प्रॉपर्टी का नाम")
area = st.text_input("एरिया (SqFt)")
loc = st.text_input("लोकेशन")
c_name = st.text_input("खरीदार")
c_phone = st.text_input("मोबाइल नंबर")
base = st.number_input("कुल राशि", value=0)
adv = st.number_input("एडवांस", value=0)

if st.button("✨ रसीद तैयार करें"):
    st.session_state.bill = {
        "id": random.randint(1000, 9999), "b_name": b_name, "area": area, 
        "loc": loc, "c_name": c_name, "c_phone": c_phone, 
        "base": base, "due": base - adv, "date": datetime.now().strftime('%d-%m-%Y')
    }

# रसीद का हिस्सा
if 'bill' in st.session_state:
    rb = st.session_state.bill
    st.markdown(f"""
    <div class="printable-area print-container">
        <h2 style="text-align:center;">MAA PROPERTIES</h2>
        <p><b>Inv:</b> {rb['id']} | <b>Date:</b> {rb['date']}</p>
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
    st.success("✅ रसीद तैयार है! अब प्रिंट करें।")
    st.info("🖨️ प्रिंट करने के लिए अपने कीबोर्ड पर Ctrl + P दबाएं।")
