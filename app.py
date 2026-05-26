import streamlit as st
import random
from datetime import datetime
import json

st.set_page_config(page_title="Maa Property 2026", layout="wide")

# डेटा को सेव रखने के लिए सेशन स्टेट
if 'bills' not in st.session_state: st.session_state.bills = []

# लॉगिन
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    u = st.text_input("यूजर आईडी")
    p = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if u == "admin" and p == "12345": st.session_state.logged_in = True; st.rerun()
    st.stop()

st.title("⚡ मां प्रॉपर्टी 2026")

# PDF जनरेटर फंक्शन (बिना किसी बाहरी लाइब्रेरी के - HTML के जरिए)
def get_pdf_html(rb):
    return f"""
    <html><body>
        <div style="border:2px solid #000; padding:20px; width:300px;">
            <h2>MAA PROPERTIES</h2>
            <p><b>Inv:</b> {rb['id']} | <b>Date:</b> {rb['date']}</p>
            <hr>
            <p><b>Property:</b> {rb['b_name']}</p>
            <p><b>Buyer:</b> {rb['c_name']}</p>
            <p><b>Total:</b> ₹{rb['base']} | <b>Due:</b> ₹{rb['due']}</p>
        </div>
    </body></html>
    """

# टैब्स
t1, t2 = st.tabs(["➕ नई रसीद", "📜 हिस्ट्री/एडिट"])

with t1:
    b_name = st.text_input("प्रॉपर्टी का नाम")
    c_name = st.text_input("खरीदार")
    base = st.number_input("कुल राशि", value=0)
    adv = st.number_input("एडवांस", value=0)
    if st.button("रसीद सेव करें"):
        new_bill = {"id": random.randint(1000,9999), "b_name": b_name, "c_name": c_name, "base": base, "due": base-adv, "date": datetime.now().strftime('%d-%m-%Y')}
        st.session_state.bills.append(new_bill)
        st.success("रसीद सेव हो गई!")

with t2:
    for i, b in enumerate(st.session_state.bills):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"🆔 {b['id']} - {b['c_name']} (बाकी: ₹{b['due']})")
        
        # एडिट फंक्शन
        if col2.button("✏️ एडिट", key=f"edit_{i}"):
            st.session_state.edit_idx = i
            
        # डिलीट फंक्शन
        if col3.button("🗑️ डिलीट", key=f"del_{i}"):
            st.session_state.bills.pop(i)
            st.rerun()

    # एडिट फॉर्म
    if 'edit_idx' in st.session_state:
        idx = st.session_state.edit_idx
        st.subheader("एडिट करें")
        st.session_state.bills[idx]['c_name'] = st.text_input("नाम बदलें", value=st.session_state.bills[idx]['c_name'])
        if st.button("सेव करें"): del st.session_state.edit_idx; st.rerun()

    # PDF डाउनलोड का सेक्शन
    st.divider()
    st.subheader("📥 रसीद डाउनलोड करें")
    for b in st.session_state.bills:
        st.download_button(f"डाउनलोड रसीद {b['id']}", get_pdf_html(b), file_name=f"bill_{b['id']}.html", mime="text/html")
