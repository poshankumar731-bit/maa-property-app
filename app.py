import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. डेटाबेस इनिशियलाइज़र (मेमोरी लॉक)
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = []

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

# मुख्य टाइटल
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# टैब नेविगेशन
tab1, tab2, tab3 = st.tabs([
    "🔍 लाइव स्क्रीन (View Database)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "💳 डिजिटल बिलिंग (Billing)"
])

# ==================== टैब 1: लाइव स्क्रीन और डिलीट लॉजिक ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    # लूप चलाकर सभी प्रॉपर्टीज को दिखाना
    for index, p in enumerate(list(st.session_state.properties)):
        col_info, col_del = st.columns([4, 1])
        
        with col_info:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
            st.write(f"👤 मालिक: {p['owner']}")
            
            msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
            wa_url = f"https://wa.me/918109471091?text={msg.replace(' ', '%20')}"
            st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            # हर प्रॉपर्टी के लिए एक यूनिक डिलीट बटन
            if st.button("❌ डिलीट करें", key=f"del_item_{p['id']}_{index}"):
                st.session_state.properties.pop(index)
                st.warning(f"🗑️ {p['name']} को सफलतापूर्वक हटा दिया गया है!")
                st.rerun()
                
        st.write("---")

# ==================== टैब 2: नई प्रॉपर्टी एंट्री फॉर्म ====================
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("property_add_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        submit_btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if submit_btn:
            if n and r:
                try:
                    price_parsed = int(r)
                except:
                    price_parsed = 0
                new_id = f"PROP-{random.randint(400, 999)}"
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": str(price_parsed), "location": l, "owner": o
                })
                st.success(f"🎉 प्रॉपर्टी '{n}' सफलतापूर्वक जोड़ दी गई है!")
                st.balloons()
                st.rerun()
            else:
                st.error("कृपया प्रॉपर्टी का नाम और कीमत भरना सुनिश्चित करें!")

# ==================== टैब 3: बिलिंग और सीधा प्रिंटर बटन ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    col_l, col_r = st.columns(2)
    
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="maa proprey")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="chatarkhar")
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value="umasankar")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value="8109471091")

    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=20000000, step=5000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0, step=1000)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=100000, step=5000)

    # कैलकुलेशन
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")

    if st.button("✨ डिजिटल रसीद तैयार करें"):
        if b_name == "":
            st.error("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम लिखें!")
        else:
            inv_id = f"INV-{random.randint(3000, 3999)}"
            st.session_state.active_bill = {
                "id": inv_id, "date": current_date, "time": current_time,
                "b_name": b_name, "b_loc": b_loc, "c_name": c_name, "c_phone": c_phone,
                "base": base_price, "disc": disc, "total": final_total, "adv": adv, "due": pending_amount
            }
            st.session_state.bill_records.append({
                "रसीद ID": inv_id, "तारीख": current_date, "प्रॉपर्टी": b_name, "कस्टमर": c_name, "बकाया राशि": pending_amount
            })
            st.success("✅ डिजिटल रसीद जनरेट हो चुकी है!")

    # बिना किसी सिंटैक्स एरर के रसीद डिस्प्ले और प्रिंट
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        
        st.write("### 🧾 जनरेटेड इनवॉइस")
        
        # प्रिंट ट्रिगर बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">🖨️ रसीद सीधे प्रिंटर से प्रिंट करें</button>', unsafe_allow_html=True)
        
        # रसीद का साफ़-सुथरा लेआउट बॉक्स
        st.info(f"📄 इनवॉइस नंबर: {rb['id']} | 📅 दिनांक: {rb['date']} | ⏰ समय: {rb['time']}")
        
        st.markdown(f"**🏢 प्रॉपर्टी:** {rb['b_name']} ({rb['b_loc']})")
        st.markdown(f"**👤 ग्राहक:** {rb['c_name']} | 📞 **मोबाइल:** {rb['c_phone']}")
        
        st.write("---")
        st.write(f"🔸 **मूल सौदा राशि:** ₹{rb['base']:,}.00")
        st.write(f"🔸 **विशेष छूट (Discount):** ₹{rb['disc']:,}.00")
        st.success(f"🔹 **कुल फाइनल सौदा मूल्य:** ₹{rb['total']:,}.00")
        st.write(f"🟩 **प्राप्त एडवांस (बयाना):** ₹{rb['adv']:,}.00")
        st.error(f"🔴 **कुल बकाया राशि (PENDING DUE):
            
