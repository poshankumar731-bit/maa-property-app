import streamlit as st
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="wide")

# 2. स्टाइलिंग और प्रिंटर सेटिंग
st.markdown("""
<style>
    .billing-app-invoice { 
        background-color: #ffffff; 
        color: #000000; 
        padding: 25px; 
        border: 2px solid #000; 
        max-width: 480px; 
        margin: 10px auto; 
    }
    @media print {
        body * { visibility: hidden; }
        .printable-area, .printable-area * { visibility: visible; }
        .printable-area { position: absolute; left: 0; top: 0; width: 100%; border: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. सेशन स्टेट (डेटा सुरक्षित रखने के लिए)
if 'generated_otp' not in st.session_state: st.session_state.generated_otp = str(random.randint(5000, 9999))
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'properties' not in st.session_state: st.session_state.properties = []
if 'active_bill' not in st.session_state: st.session_state.active_bill = None

# 4. लॉगिन सिस्टम
if not st.session_state.logged_in:
    st.markdown("### 🔐 लॉगिन")
    st.warning(f"🔑 OTP: {st.session_state.generated_otp}")
    mobile = st.text_input("मोबाइल नंबर", value="8109471091")
    otp_input = st.text_input("OTP डालें", type="password")
    if st.button("🔓 लॉगिन"):
        if otp_input == st.session_state.generated_otp:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("गलत OTP!")
    st.stop()

# 5. मुख्य ऐप
st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

tab1, tab2, tab3 = st.tabs(["🔍 प्रॉपर्टीज", "➕ नई एंट्री", "💳 बिलिंग"])

with tab1:
    st.write("आपकी प्रॉपर्टीज यहाँ दिखेंगी")
    for i, p in enumerate(st.session_state.properties):
        st.info(f"{p['name']} | {p['location']}")

with tab2:
    with st.form("p_form"):
        n = st.text_input("प्रॉपर्टी नाम")
        l = st.text_input("लोकेशन")
        if st.form_submit_button("सेव"):
            st.session_state.properties.append({"name": n.upper(), "location": l.upper()})
            st.success("जुड़ गया!")

with tab3:
    b_name = st.text_input("प्रॉपर्टी नाम", value="MAA PROPERTY")
    c_name = st.text_input("खरीदार का नाम", value="CLIENT")
    base = st.number_input("कुल राशि", value=2000000)
    adv = st.number_input("एडवांस", value=100000)
    
    if st.button("✨ रसीद जेनरेट करें"):
        st.session_state.active_bill = {
            "id": random.randint(3000, 9999), 
            "b_name": b_name.upper(), 
            "c_name": c_name.upper(), 
            "base": base, 
            "adv": adv, 
            "due": base-adv
        }

    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.markdown(f"""
        <div class="printable-area billing-app-invoice">
            <h2 style="text-align:center;">MAA PROPERTIES</h2>
            <p><b>Invoice No:</b> {rb['id']} &nbsp;&nbsp; <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}</p>
            <hr>
            <p><b>Property:</b> {rb['b_name']}</p>
            <p><b>Buyer:</b> {rb['c_name']}</p>
            <p><b>Total Amount:</b> ₹{rb['base']:,}</p>
            <p><b>Advance Paid:</b> ₹{rb['adv']:,}</p>
            <p><b>Balance Due:</b> ₹{rb['due']:,}</p>
            <br><br>
            <table width="100%">
                <tr>
                    <td align="left">_______<br><b>Buyer Sign</b></td>
                    <td align="right">_______<br><b>Seller Sign</b></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 अब कीबोर्ड पर Ctrl + P दबाएं और केवल बिल प्रिंट करें!")
