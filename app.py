import streamlit as st
import random
from datetime import datetime

# 1. पेज सेटअप - लेआउट को थोड़ा संकुचित किया ताकि प्रिंटिंग में दिक्कत न हो
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# 2. CSS - यह बिल को एक ही पेज पर फिक्स रखेगा और प्रिंट बटन को हटा देगा
st.markdown("""
<style>
    .billing-app-invoice { 
        background-color: #ffffff; 
        color: #000000; 
        padding: 20px; 
        border: 2px solid #000; 
        max-width: 450px; 
        margin: 0 auto; 
    }
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
        @page { size: auto; margin: 5mm; }
    }
    .stApp { max-width: 800px; margin: auto; }
</style>
""", unsafe_allow_html=True)

# 3. सुरक्षा - लॉगिन पासवर्ड फिक्स रखें
PASSWORD = "123" # अपना पासवर्ड यहाँ बदल सकते हैं

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'bill_records' not in st.session_state: st.session_state.bill_records = []
if 'active_bill' not in st.session_state: st.session_state.active_bill = None

# लॉगिन स्क्रीन
if not st.session_state.logged_in:
    st.subheader("🔐 मां प्रॉपर्टी - लॉगिन")
    pwd = st.text_input("पासवर्ड डालें", type="password")
    if st.button("लॉगिन करें"):
        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("गलत पासवर्ड!")
    st.stop()

# मुख्य ऐप
st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

tab1, tab2 = st.tabs(["💳 नई रसीद", "📜 हिस्ट्री"])

with tab1:
    b_name = st.text_input("प्रॉपर्टी का नाम")
    area = st.text_input("एरिया (SqFt)")
    loc = st.text_input("जमीन कहाँ की है")
    c_name = st.text_input("खरीदार का नाम")
    c_phone = st.text_input("मोबाइल नंबर")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)
    
    if st.button("✨ रसीद जेनरेट करें"):
        new_bill = {"id": random.randint(1000, 9999), "b_name": b_name.upper(), "area": area, "loc": loc.upper(), 
                    "c_name": c_name.upper(), "c_phone": c_phone, "base": base, "adv": adv, "due": base-adv}
        st.session_state.active_bill = new_bill
        st.session_state.bill_records.append(new_bill)

    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.markdown(f"""
        <div class="printable-area billing-app-invoice">
            <h3 style="text-align:center;">MAA PROPERTIES</h3>
            <p><b>Inv:</b> {rb['id']} | <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}</p>
            <hr>
            <p><b>Property:</b> {rb['b_name']}</p>
            <p><b>Area:</b> {rb['area']} SqFt</p>
            <p><b>Location:</b> {rb['loc']}</p>
            <p><b>Buyer:</b> {rb['c_name']}</p>
            <p><b>Mobile:</b> {rb['c_phone']}</p>
            <p><b>Total:</b> ₹{rb['base']:,} | <b>Due:</b> ₹{rb['due']:,}</p>
            <br><br>
            <table width="100%"><tr><td>_______<br>Buyer</td><td align="right">_______<br>Seller</td></tr></table>
        </div>
        """, unsafe_allow_html=True)
        st.info("🖨️ प्रिंट करने के लिए Ctrl + P दबाएं।")

with tab2:
    st.subheader("📜 बिल हिस्ट्री")
    for r in reversed(st.session_state.bill_records):
        st.write(f"🆔 {r['id']} | 👤 {r['c_name']} | 🏢 {r['b_name']} | 🔴 बकाया: ₹{r['due']:,}")
