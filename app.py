import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. डेटाबेस (मेमोरी लॉक)
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

# तीन आसान टैब
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (View Database)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग (Billing)"])

# ==================== टैब 1: लाइव स्क्रीन (प्रॉपर्टी लिस्ट और डिलीट) ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    # सुरक्षित तरीके से लिस्ट दिखाने और डिलीट करने का लॉजिक
    props_list = list(st.session_state.properties)
    for index, p in enumerate(props_list):
        col_info, col_del = st.columns([4, 1])
        
        with col_info:
            st.info("🏢 नाम: " + str(p['name']) + " | ID: " + str(p['id']) + " | प्रकार: " + str(p['type']))
            st.write("📍 लोकेशन: " + str(p['location']) + " | 📐 एरिया: " + str(p['area']) + " | 💰 कीमत: ₹" + str(p['rate']))
            st.write("👤 मालिक: " + str(p['owner']))
            
            # व्हाट्सएप लिंक जनरेटर
            msg = "नमस्ते, मुझे आपकी प्रॉपर्टी " + str(p['name']) + " में इंटरेस्ट है।"
            wa_url = "https://wa.me/918109471091?text=" + msg.replace(" ", "%20")
            st.markdown("[💬 WhatsApp पर विवरण भेजें](" + wa_url + ")")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            # हर आइटम का अपना यूनिक बटन
            btn_key = "del_" + str(p['id']) + "_" + str(index)
            if st.button("❌ डिलीट करें", key=btn_key):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी को हटा दिया गया है!")
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
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
                })
                st.success("🎉 प्रॉपर्टी डेटाबेस में जोड़ दी गई है!")
                st.balloons()
                st.rerun()
            else:
                st.error("कृपया प्रॉपर्टी का नाम और कीमत जरूर भरें!")

# ==================== टैब 3: बिलिंग और प्रिंट आउट ====================
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

    # साधारण बिना एरर वाली कैलकुलेशन
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")

    if st.button("✨ डिजिटल रसीद तैयार करें"):
        if b_name == "":
            st.error("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम लिखें!")
        else:
            inv_id = "INV-" + str(random.randint(3000, 3999))
            st.session_state.active_bill = {
                "id": inv_id, "date": current_date, "time": current_time,
                "b_name": b_name, "b_loc": b_loc, "c_name": c_name, "c_phone": c_phone,
                "base": base_price, "disc": disc, "total": final_total, "adv": adv, "due": pending_amount
            }
            st.session_state.bill_records.append({
                "रसीद ID": inv_id, "तारीख": current_date, "प्रॉपर्टी": b_name, "कस्टमर": c_name, "बकाया राशि": pending_amount
            })
            st.success("✅ डिजिटल रसीद तैयार! नीचे प्रिंट बटन दबाएं।")

    # रसीद दिखाने का सबसे सुरक्षित तरीका (बिना किसी String Literal Error के)
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        
        st.write("### 🧾 || मां प्रॉपर्टीज इनवॉइस ||")
        
        # सीधा ब्राउज़र/थर्मल प्रिंट कमांड बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 12px 25px; border: none; border-radius: 4px; cursor: pointer; width: 100%;">🖨️ रसीद का पेपर प्रिंट आउट निकालें</button>', unsafe_allow_html=True)
        st.write(" ")
        
        # साफ-सुथरा बिना उलझन का लेआउट बॉक्स
        st.info("📄 इनवॉइस नंबर: " + str(rb['id']) + "  |  📅 दिनांक: " + str(rb['date']) + "  |  ⏰ समय: " + str(rb['time']))
        
        st.write("🏢 **प्रॉपर्टी का नाम:** " + str(rb['b_name']))
        st.write("📍 **लोकेशन:** " + str(rb['b_loc']))
        st.write("👤 **ग्राहक का नाम:** " + str(rb['c_name']))
        st.write("📞 **मोबाइल नंबर:** " + str(rb['c_phone']))
        
        st.write("---")
        st.write("🔸 **मूल सौदा राशि:** ₹" + str(rb['base']))
        st.write("🔸 **विशेष छूट (Discount):** ₹" + str(rb['disc']))
        st.success("🔹 **कुल फाइनल सौदा मूल्य:** ₹" + str(rb['total']))
        st.write("🟩 **प्राप्त एडवांस राशि:** ₹" + str(rb['adv']))
        st.error("🔴 **कुल बकाया राशि (PENDING DUE):** ₹" + str(rb['due']))
        st.write("---")

    # सुरक्षित बिल रिकॉर्ड रजिस्टर हिस्ट्री
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    if len(st.session_state.bill_records) > 0:
        st.dataframe(pd.DataFrame(st.session_state.bill_records), use_container_width=True)
