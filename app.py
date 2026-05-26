import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. सुरक्षित डेटाबेस मेमोरी लॉक (रजिस्टर होल्ड)
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

# मुख्य टाइटल
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# तीन आसान टैब नेविगेशन
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (Properties)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग एवं रजिस्टर"])

# ==================== टैब 1: लाइव प्रॉपर्टी लिस्ट ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    p_list = list(st.session_state.properties)
    for index, p in enumerate(p_list):
        col_info, col_del = st.columns([4, 1])
        with col_info:
            st.info("🏢 नाम: " + str(p['name']) + " | ID: " + str(p['id']) + " | प्रकार: " + str(p['type']))
            st.write("📍 लोकेशन: " + str(p['location']) + " | 📐 एरिया: " + str(p['area']) + " | 💰 कीमत: ₹" + str(p['rate']))
            st.write("👤 मालिक: " + str(p['owner']))
        with col_del:
            st.write(" ")
            st.write(" ")
            if st.button("❌ हटाएँ", key="del_p_" + str(index)):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी हटा दी गई है!")
                st.rerun()
        st.write("---")

# ==================== टैब 2: नई प्रॉपर्टी फॉर्म ====================
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        if st.form_submit_button("☁️ सुरक्षित लाइव सेव करें"):
            if n and r:
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
                })
                st.success("🎉 सफलतापूर्वक लाइव सुरक्षित कर दी गई है!")
                st.rerun()

# ==================== टैब 3: डिजिटल बिलिंग और सुरक्षित रिकॉर्ड रजिस्टर ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    # एडिट मोड चेकिंग
    is_edit = st.session_state.edit_index is not None
    if is_edit:
        st.warning("⚠️ आप रिकॉर्ड रजिस्टर में पुराने बिल को बदल (Edit) रहे हैं!")
        edit_data = st.session_state.bill_records[st.session_state.edit_index]
        v_bname, v_bloc, v_cname, v_cphone = edit_data["प्रॉपर्टी_नाम"], edit_data["लोकेशन"], edit_data["ग्राहक_नाम"], edit_data["मोबाइल"]
        v_base, v_disc, v_adv = int(edit_data["मूल_राशि"]), int(edit_data["छूट"]), int(edit_data["एडवांस"])
    else:
        v_bname, v_bloc, v_cname, v_cphone = "maa proprey", "chatarkhar", "umasankar", "8109471091"
        v_base, v_disc, v_adv = 20000000, 0, 100000

    col_l, col_r = st.columns(2)
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value=v_bname)
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value=v_bloc)
        c_name = st.text_input("3. ग्राहक का नाम", value=v_cname)
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value=v_cphone)
    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=v_base)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=v_disc)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=v_adv)

    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write(" ")
    
    if is_edit:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("💾 एडिट किया हुआ बिल अपडेट करें", type="primary"):
                idx = st.session_state.edit_index
                st.session_state.bill_records[idx] = {
                    "रसीद_ID": edit_data["रसीद_ID"], "तारीख": edit_data["तारीख"],
                    "प्रॉपर्टी_नाम": b_name, "लोकेशन": b_loc, "ग्राहक_नाम": c_name, "मोबाइल": c_phone,
                    "मूल_राशि": base_price, "छूट": disc, "एडवांस": adv, "कुल_बकाया": pending_amount
                }
                st.session_state.active_bill = st.session_state.bill_records[idx]
                st.session_state.edit_index = None
                st.success("✅ रिकॉर्ड सफलतापूर्वक अपडेट हो गया!")
                st.rerun()
        with col_e2:
            if st.button("❌ बदलाव रद्द करें"):
                st.session_state.edit_index = None
                st.rerun()
    else:
        if st.button("✨ नई डिजिटल रसीद तैयार करें", type="primary"):
            if b_name:
                inv_id = "INV-" + str(random.randint(3000, 3999))
                new_bill = {
                    "रसीद_ID": inv_id, "तारीख": current_date, "समय": current_time,
                    "प्रॉपर्टी_नाम": b_name, "लोकेशन": b_loc, "ग्राहक_नाम": c_name, "मोबाइल": c_phone,
                    "मूल_राशि": base_price, "छूट": disc, "एडवांस": adv, "कुल_बकाया": pending_amount
                }
                st.session_state.active_bill = new_bill
                st.session_state.bill_records.append(new_bill)
                st.success("✅ नई रसीद रजिस्टर में सुरक्षित हो चुकी है!")

    # ==================== रसीद का रियल प्रिंटर लेआउट ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 जनरेटेड डिजिटल रसीद (प्रिंटर रेडी कॉपी)")
        
        # 🖨️ कंप्यूटर या मोबाइल से डायरेक्ट प्रिंट आउट निकालने का बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 15px 30px; border: 2px solid black; border-radius: 5px; cursor: pointer; width: 100%; font-size: 18px;">🖨️ यहाँ क्लिक करके तुरंत रसीद प्रिंटर से बाहर निकालें</button>', unsafe_allow_html=True)
        st.write(" ")
        
        # रसीद स्लिप बॉक्स
        st.info("📄 रसीद ID: " + str(rb['रसीद_ID']) + "  |  📅 तारीख: " + str(rb['तारीख']))
        st.write("🏢 **प्रॉपर्टी:** " + str(rb['प्रॉपर्टी_नाम']) + " (" + str(rb['लोकेशन']) + ")")
        st.write("👤 **ग्राहक:** " + str(rb['ग्राहक_नाम']) + "  |  📞 **मोबाइल:** " + str(rb['मोबाइल']))
        st.write("---")
        st.write("🔸 मूल सौदा राशि: ₹" + str(rb['मूल_राशि']))
        st.write("🔸 विशेष छूट (Discount): ₹" + str(rb['छूट']))
        st.success("🔹 कुल फाइनल मूल्य: ₹" + str(rb['मूल_राशि'] - rb['छूट']))
        st.write("🟩 प्राप्त एडवांस राशि: ₹" + str(rb['एडवांस']))
        st.error("🔴 कुल बकाया राशि (PENDING DUE): ₹" + str(rb['कुल_बकाया']))
        st.write("---")
        st.caption("Verified by Maa Property Cloud 2026")

    # ==================== सुरक्षित बिल रिकॉर्ड रजिस्टर (एडिट + डिलीट ऑप्शन) ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    
    r_list = list(st.session_state.bill_records)
    if len(r_list) > 0:
        for r_idx, r_data in enumerate(r_list):
            col_rec_info, col_rec_edit, col_rec_del = st.columns([3, 1, 1])
            
            with col_rec_info:
                st.code("🆔 " + str(r_data['रसीद_ID']) + " | 👤 " + str(r_data['ग्राहक_नाम']) + " | 🏢 " + str(r_data['प्रॉपर्टी_नाम']) + " | 🔴 बकाया: ₹" + str(r_data['कुल_बकाया']))
            
            with col_rec_edit:
                if st.button("✏️ एडिट करें", key="edit_b_" + str(r_idx)):
                    st.session_state.edit_index = r_idx
                    st.rerun()
                    
            with col_rec_del:
                if st.button("🗑️ डिलीट", key="del_b_" + str(r_idx)):
                    st.session_state.bill_records.pop(r_idx)
                    st.session_state.active_bill = None
                    st.warning("🗑️ रसीद को रजिस्टर से डिलीट कर दिया गया है!")
                    st.rerun()
    else:
        st.write("अभी कोई रिकॉर्ड सुरक्षित नहीं है।")
