import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप (Full Screen Layout)
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. डेटाबेस मेमोरी लॉक (ताकि डेटा डिलीट न हो)
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = [
        {"रसीद_ID": "INV-3012", "तारीख": "26-05-2026", "प्रॉपर्टी_नाम": "Maa Property", "लोकेशन": "Chatarkhar", "ग्राहक_नाम": "Umasankar", "मोबाइल": "8109471091", "मूल_राशि": 20000000, "छूट": 0, "एडवांस": 100000, "कुल_बकाया": 19900000}
    ]

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# मुख्य ऐप टाइटल
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# तीन आसान टैब सिस्टम
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (Properties)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग एवं रजिस्टर (Billing & Records)"])

# ==================== टैब 1: लाइव प्रॉपर्टी स्क्रीन ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    for index, p in enumerate(list(st.session_state.properties)):
        col_info, col_del = st.columns([4, 1])
        with col_info:
            st.info("🏢 नाम: " + str(p['name']) + " | ID: " + str(p['id']) + " | प्रकार: " + str(p['type']))
            st.write("📍 लोकेशन: " + str(p['location']) + " | 📐 एरिया: " + str(p['area']) + " | 💰 कीमत: ₹" + str(p['rate']))
            st.write("👤 मालिक: " + str(p['owner']))
            
            msg = "नमस्ते, मुझे आपकी प्रॉपर्टी " + str(p['name']) + " में इंटरेस्ट है।"
            wa_url = "https://wa.me/918109471091?text=" + msg.replace(" ", "%20")
            st.markdown("[💬 WhatsApp पर विवरण भेजें](" + wa_url + ")")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            if st.button("❌ प्रॉपर्टी हटाएँ", key="del_prop_" + str(p['id']) + "_" + str(index)):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी हटा दी गई है!")
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
                st.success("🎉 नई प्रॉपर्टी सफलतापूर्वक लाइव सुरक्षित कर दी गई है!")
                st.balloons()
                st.rerun()
            else:
                st.error("कृपया प्रॉपर्टी का नाम और कीमत भरना अनिवार्य है!")

# ==================== टैब 3: डिजिटल बिलिंग और सुरक्षित रिकॉर्ड रजिस्टर ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    # अगर कोई बिल एडिट मोड में है तो उसकी वैल्यू फॉर्म में पहले से दिखाई देगी
    is_edit = st.session_state.edit_index is not None
    if is_edit:
        st.warning("⚠️ आप अभी रिकॉर्ड रजिस्टर में पुराने बिल को बदल (Edit) रहे हैं!")
        edit_data = st.session_state.bill_records[st.session_state.edit_index]
        default_bname = edit_data["प्रॉपर्टी_नाम"]
        default_bloc = edit_data["लोकेशन"]
        default_cname = edit_data["ग्राहक_नाम"]
        default_cphone = edit_data["मोबाइल"]
        default_base = int(edit_data["मूल_राशि"])
        default_disc = int(edit_data["छूट"])
        default_adv = int(edit_data["एडवांस"])
    else:
        default_bname = "maa proprey"
        default_bloc = "chatarkhar"
        default_cname = "umasankar"
        default_cphone = "8109471091"
        default_base = 20000000
        default_disc = 0
        default_adv = 100000

    col_l, col_r = st.columns(2)
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value=default_bname)
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value=default_bloc)
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value=default_cname)
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value=default_cphone)

    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=default_base, step=5000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=default_disc, step=1000)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=default_adv, step=5000)

    # कैलकुलेशन
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write(" ")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if is_edit:
            if st.button("💾 एडिट किया हुआ बिल अपडेट करें", type="primary"):
                idx = st.session_state.edit_index
                st.session_state.bill_records[idx] = {
                    "रसीद_ID": edit_data["रसीद_ID"], "तारीख": edit_data["तारीख"],
                    "प्रॉपर्टी_नाम": b_name, "लोकेशन": b_loc, "ग्राहक_नाम": c_name, "मोबाइल": c_phone,
                    "मूल_राशि": base_price, "छूट": disc, "एडवांस": adv, "कुल_बकाया": pending_amount
                }
                st.session_state.active_bill = st.session_state.bill_records[idx]
                st.session_state.edit_index = None # एडिट समाप्त
                st.success("✅ पुराना रिकॉर्ड सफलतापूर्वक अपडेट (Edit) कर दिया गया है!")
                st.rerun()
        else:
            if st.button("✨ नई डिजिटल रसीद तैयार करें", type="primary"):
                if b_name == "":
                    st.error("कृपया प्रॉपर्टी का नाम लिखें!")
                else:
                    inv_id = "INV-" + str(random.randint(3000, 3999))
                    new_bill = {
                        "रसीद_ID": inv_id, "तारीख": current_date, "समय": current_time,
                        "प्रॉपर्टी_नाम": b_name, "लोकेशन": b_loc, "ग्राहक_नाम": c_name, "मोबाइल": c_phone,
                        "मूल_राशि": base_price, "छूट": disc, "एडवांस": adv, "कुल_बकाया": pending_amount
                    }
                    st.session_state.active_bill = new_bill
                    st.session_state.bill_records.append({
                        "रसीद_ID": inv_id, "तारीख": current_date, "प्रॉपर्टी_नाम": b_name, "लोकेशन": b_loc,
                        "ग्राहक_नाम": c_name, "मोबाइल": c_phone, "मूल_राशि": base_price, "छूट": disc, "एडवांस": adv, "कुल_बकाया": pending_amount
                    })
                    st.success("✅ नई डिजिटल रसीद रजिस्टर में सुरक्षित हो चुकी है!")

    with col_btn2:
        if is_edit:
            if st.button("❌ बदलाव रद्द करें (Cancel Edit)"):
                st.session_state.edit_index = None
                st.rerun()

    # ==================== रसीद का सुंदर प्रिंटर लेआउट बॉक्स ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 जनरेटेड डिजिटल रसीद")
        
        # 🖨️ एक क्लिक पर प्रिंटर एक्टिव करने वाला असली बटन (Asli Window Print Command)
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 14px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; margin-bottom: 15px;">🖨️ यहाँ क्लिक करके तुरंत रसीद प्रिंट आउट निकालें</button>', unsafe_allow_html=True)
        
        # साफ़-सुथरा रसीद डिज़ाइन बॉक्स
        st.info("📄 रसीद ID: " + str(rb['रसीद_ID']) + "  |  📅 तारीख: " + str(rb['तारीख']))
        st.write("🏢 **प्रॉपर्टी का नाम:** " + str(rb['प्रॉपर्टी_नाम']) + " (" + str(rb['लोकेशन']) + ")")
        st.write("👤 **ग्राहक का नाम:** " + str(rb['ग्राहक_नाम']) + "  |  📞 **मोबाइल:** " + str(rb['मोबाइल']))
        
        st.write("---")
        st.write("🔸 मूल सौदा राशि: ₹" + str(rb['मूल_राशि']))
        st.write("🔸 विशेष छूट (Discount): ₹" + str(rb['छूट']))
        st.success("🔹 कुल फाइनल सौदा मूल्य: ₹" + str(rb['मूल_राशि'] - rb['छूट']))
        st.write("🟩 प्राप्त एडवांस (बयाना राशि): ₹" + str(rb['एडवांस']))
        st.error("🔴 कुल बकाया राशि (PENDING DUE): ₹" + str(rb['कुल_बकाया']))
        st.write("---")
        st.caption("Verified by Maa Property Cloud 2026")

    # ==================== सुरक्षित बिल रिकॉर्ड रजिस्टर (डिलीट + एडिट फीचर्स के साथ) ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    st.write("यहाँ आपके सभी पुराने बिल सुरक्षित हैं। आप किसी भी बिल को कभी भी डिलीट या एडिट कर सकते हैं:")
    
    if len(st.session_state.bill_records) > 0:
        for r_idx, r_data in enumerate(list(st.session_state
