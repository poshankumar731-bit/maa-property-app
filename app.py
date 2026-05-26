import streamlit as st
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="centered")

# 2. सुरक्षित लॉगिन क्रेडेंशियल्स
USER_DATA = {
    "admin": "MaaProperty@2026", # यूजरनेम: admin, पासवर्ड: MaaProperty@2026
    "staff": "Staff@123"          # दूसरा यूजर भी बना सकते हैं
}

# 3. सेशन स्टेट
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'bill_records' not in st.session_state: st.session_state.bill_records = []
if 'active_bill' not in st.session_state: st.session_state.active_bill = None

# लॉगिन स्क्रीन
if not st.session_state.logged_in:
    st.subheader("🔐 मां प्रॉपर्टीज - सुरक्षित लॉगिन")
    username = st.text_input("👤 यूजरनेम (Username)")
    password = st.text_input("🔑 पासवर्ड (Password)", type="password")
    
    if st.button("लॉगिन करें"):
        if username in USER_DATA and USER_DATA[username] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ गलत यूजरनेम या पासवर्ड!")
    st.stop()

# मुख्य ऐप (सिर्फ लॉगिन के बाद ही दिखेगा)
st.title("⚡ मां प्रॉपर्टी 2026")
if st.button("🔒 लॉगआउट"): st.session_state.logged_in = False; st.rerun()

# [नोट: यहाँ से नीचे आपका वही पुराना रसीद और हिस्ट्री वाला कोड रहेगा]
# कोड की लंबाई की वजह से यहाँ मैंने स्ट्रक्चर दिया है, 
# आप ऊपर के 'लॉगिन वाले हिस्से' को अपने कोड में इसी तरह बदल लें।
