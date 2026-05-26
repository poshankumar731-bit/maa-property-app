import streamlit as st
import random
from datetime import datetime

# पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# CSS: यह प्रिंटर के लिए बिल को एक पेज पर सेट करता है
st.markdown("""
<style>
    .print-container { width: 100%; max-width: 400px; border: 2px solid #000; padding: 20px; margin: auto; font-family: sans-serif; }
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# लॉगिन सिस्टम (यूजर आईडी और पासवर्ड के साथ)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 मां प्रॉपर्टी - लॉगिन")
    # यहाँ यूजर आईडी और पासवर्ड दोनों हैं
    user_id = st.text_input("👤 यूजर आईडी (User ID)")
    password = st.text_input("🔑 पासवर्ड (Password)", type="password")
    
    if st.button("लॉगिन करें"):
        if user_id == "admin" and password == "12345":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ गलत यूजर आईडी या पासवर्ड!")
    st.stop()

# मुख्य ऐप
st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

# रसीद बनाने का फॉर्म
col1, col2 = st.columns(2)
with col1:
    b_name = st.text_input("प्रॉपर्टी का नाम")
    area = st.text_input("एरिया (SqFt)")
    loc = st.text_input("लोकेशन")
with col2:
    c_name = st.text_input("खरीदार")
    c_phone = st.text_input("मोबाइल नंबर")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)

if st.button("✨ रसीद जेनरेट करें"):
    st.session_state.bill = {
        "id": random.randint(1000, 9999), "b_name": b_name, "area": area, 
        "loc": loc, "c_name": c_name, "c_phone": c_phone, 
        "base": base, "due": base - adv, "date": datetime.now().strftime('%d-%m-%Y')
    }

# बिल दिखाना और प्रिंट बटन
if 'bill' in st.session_state:
    rb = st.session_state.bill
    st.markdown(f"""
    <div class="printable-area print-container" id="receipt">
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
    
    st.write("")
    # प्रिंट बटन - इसे दबाते ही ब्राउज़र का प्रिंट डायलॉग खुलेगा
    st.markdown("""
    <button onclick="window.print()" style="width:100%; padding:10px; background-color:blue; color:white; border:none; cursor:pointer; font-size:16px;">
        🖨️ यहाँ क्लिक करके बिल प्रिंट करें
    </button>
    """, unsafe_allow_html=True)
