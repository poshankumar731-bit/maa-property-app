import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="मां प्रॉपर्टी ऐप 2026", layout="wide")

# Internal Database
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]

st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (View)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग (Billing)"])

# TAB 1: LIVE DATABASE VIEW
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    for p in st.session_state.properties:
        st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
        st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
        st.write(f"👤 मालिक: {p['owner']}")
        
        # WhatsApp Share Link
        msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर ग्राहक को विवरण भेजें]({wa_url})")
        st.write("---")

# TAB 2: ADD NEW PROPERTY
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("add_property_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if btn:
            if n and r:
                new_id = f"PROP-{random.randint(103, 999)}"
                st.session_state.properties.append({"id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o})
                st.success(f"🎉 प्रॉपर्टी सफलतापूर्वक लाइव स्क्रीन पर सेव हो गई! ID: {new_id}")
                st.balloons()
            else:
                st.error("नाम और कीमत भरना जरूरी है!")

# TAB 3: BLANK DIGITAL BILLING PANEL
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    st.write("नीचे सभी जगह खाली है, अपनी ज़रूरत के अनुसार भरें:")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", key="b_name")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", key="b_loc")
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", key="c_name")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", key="c_phone")

    with col_right:
        base_price = st.number_input("5. कुल सौदा राशि (₹)", min_value=0, value=0)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=0)

    # Invoice Calculations
    final_total = base_price - disc
    pending_amount = final_total - adv
    
    st.write("---")
    if st.button("🖨️ डिजिटल रसीद प्रिंट करें"):
        if b_name == "":
            st.warning("कृपया बिल जनरेट करने के लिए प्रॉपर्टी का नाम अवश्य लिखें!")
        else:
            st.success("⚡ || माँ प्रॉपर्टीज डिजिटल इनवॉइस ||")
            st.code(f"""
========================================
       MAA PROPERTIES DIGITAL INVOICE
========================================
तारीख: {datetime.now().strftime('%d-%m-%Y')} | समय: {datetime.now().strftime('%H:%M')}
----------------------------------------
🏢 प्रॉपर्टी: {b_name}
📍 लोकेशन : {b_loc}
👤 ग्राहक   : {c_name}
📞 मोबाइल  : {c_phone}
----------------------------------------
💵 मूल सौदा राशि  : ₹{base_price:,}
📉 डिस्काउंट छूट  : ₹{disc:,}
🟢 फाइनल सौदा मूल्य: ₹{final_total:,}
🔵 प्राप्त एडवांस  : ₹{adv:,}
========================================
🔴 कुल बकाया राशि : ₹{pending_amount:,}
========================================
   Verified by Maa Property Cloud 2026
            """)
