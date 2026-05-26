import streamlit as st
import random
from datetime import datetime

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

tab1, tab2 = st.tabs(["💳 नई रसीद", "📜 बिल हिस्ट्री"])

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
            "base": base, "adv": adv, "due": base-adv, "date": datetime.now().strftime('%d-%m-%Y')
        }
        
        # नए पेज के लिए HTML (प्रिंट के लिए एकदम परफेक्ट)
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; padding: 20px; }}
                .receipt {{ width: 100%; max-width: 400px; border: 2px solid #000; padding: 20px; }}
                h2 {{ text-align: center; margin-top: 0; }}
                .row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
            </style>
        </head>
        <body onload="window.print()">
            <div class="receipt">
                <h2>MAA PROPERTIES</h2>
                <hr>
                <p><b>Inv:</b> {bill_data['id']} | <b>Date:</b> {bill_data['date']}</p>
                <p><b>Property:</b> {bill_data['b_name']}</p>
                <p><b>Area:</b> {bill_data['area']} SqFt</p>
                <p><b>Location:</b> {bill_data['loc']}</p>
                <p><b>Buyer:</b> {bill_data['c_name']}</p>
                <p><b>Mobile:</b> {bill_data['c_phone']}</p>
                <hr>
                <p><b>Total:</b> ₹{bill_data['base']:,}</p>
                <p><b>Due:</b> ₹{bill_data['due']:,}</p>
                <br><br>
                <div style="display:flex; justify-content: space-between;">
                    <span>_______<br>Buyer</span>
                    <span>_______<br>Seller</span>
                </div>
            </div>
        </body>
        </html>
        """
        
        # नया टैब खोलने का तरीका
        import base64
        b64 = base64.b64encode(html_code.encode()).decode()
        st.write(f'<a href="data:text/html;base64,{b64}" target="_blank" style="font-size:20px; color:green;">🖨️ रसीद नए पेज में खुल गई है! (यदि नहीं तो यहाँ क्लिक करें)</a>', unsafe_allow_html=True)
        
        if 'bill_records' not in st.session_state: st.session_state.bill_records = []
        st.session_state.bill_records.append(bill_data)

with tab2:
    st.subheader("📜 पिछले बिलों की हिस्ट्री")
    if 'bill_records' in st.session_state:
        for r in reversed(st.session_state.bill_records):
            st.write(f"🆔 {r['id']} | 👤 {r['c_name']} | 🏢 {r['b_name']} | 🔴 बकाया: ₹{r['due']:,}")
