import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप (Full Screen)
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. डेटाबेस मेमोरी लॉक (KeyError को रोकने के लिए फिक्स्ड इंग्लिश कॉलम्स)
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = [
        {"bill_id": "INV-3012", "date": "26-05-2026", "prop_name": "Maa Property", "location": "Chatarkhar", "cust_name": "Umasankar", "phone": "8109471091", "base": 20000000, "disc": 0, "adv": 100000, "due": 19900000}
    ]

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# मुख्य ऐप का हेडर
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# तीन साफ़ टैब सिस्टम
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (Properties)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग एवं रिकॉर्ड रजिस्टर"])

# ==================== टैब 1: लाइव प्रॉपर्टी स्क्रीन ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    props = list(st.session_state.properties)
    for index, p in enumerate(props):
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
            if st.button("❌ प्रॉपर्टी हटाएँ", key="del_property_" + str(index)):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी हटा दी गई है!")
                st.rerun()
        st.write("---")

# ==================== टैब 2: नई प्रॉपर्टी एंट्री फॉर्म ====================
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("property_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        if st.form_submit_button("☁️ सुरक्षित लाइव सेव करें"):
            if n and r:
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
                })
                st.success("🎉 नई प्रॉपर्टी सुरक्षित कर दी गई है!")
                st.rerun()

# ==================== टैब 3: डिजिटल बिलिंग और सुरक्षित रिकॉर्ड रजिस्टर ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    # एडिट मोड इंडेक्स चेकिंग
    is_edit = st.session_state.edit_index is not None
    if is_edit:
        st.warning("⚠️ आप अभी रिकॉर्ड रजिस्टर में पुराने बिल में बदलाव (Edit) कर रहे हैं!")
        edit_data = st.session_state.bill_records[st.session_state.edit_index]
        v_bname, v_bloc, v_cname, v_cphone = edit_data["prop_name"], edit_data["location"], edit_data["cust_name"], edit_data["phone"]
        v_base, v_disc, v_adv = int(edit_data["base"]), int(edit_data["disc"]), int(edit_data["adv"])
    else:
        v_bname, v_bloc, v_cname, v_cphone = "maa proprey", "chatarkhar", "umasankar", "8109471091"
        v_base, v_disc, v_adv = 20000000, 0, 100000

    col_l, col_r = st.columns(2)
    with col_l:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value=v_bname)
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value=v_bloc)
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value=v_cname)
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value=v_cphone)

    with col_r:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=v_base)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=v_disc)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=v_adv)

    # फिक्स्ड कैलकुलेशन
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    
    st.write(" ")
    
    if is_edit:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("💾 एडिट किया हुआ बिल अपडेट करें", type="primary"):
                idx = st.session_state.edit_index
                updated_bill = {
                    "bill_id": edit_data["bill_id"], "date": edit_data["date"],
                    "prop_name": b_name, "location": b_loc, "cust_name": c_name, "phone": c_phone,
                    "base": base_price, "disc": disc, "adv": adv, "due": pending_amount
                }
                st.session_state.bill_records[idx] = updated_bill
                st.session_state.active_bill = updated_bill
                st.session_state.edit_index = None
                st.success("✅ पुराना रिकॉर्ड रजिस्टर में अपडेट हो गया है!")
                st.rerun()
        with col_e2:
            if st.button("❌ बदलाव रद्द करें"):
                st.session_state.edit_index = None
                st.rerun()
    else:
        if st.button("✨ नई डिजिटल रसीद तैयार करें", type="primary"):
            if b_name == "":
                st.error("कृपया प्रॉपर्टी का नाम लिखें!")
            else:
                inv_id = "INV-" + str(random.randint(3000, 3999))
                new_bill = {
                    "bill_id": inv_id, "date": current_date,
                    "prop_name": b_name, "location": b_loc, "cust_name": c_name, "phone": c_phone,
                    "base": base_price, "disc": disc, "adv": adv, "due": pending_amount
                }
                st.session_state.active_bill = new_bill
                st.session_state.bill_records.append(new_bill)
                st.success("✅ नई डिजिटल रसीद रजिस्टर में सुरक्षित हो चुकी है!")

    # ==================== रसीद का सुंदर प्रिंटर लेआउट (KeyError फिक्स्ड) ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 जनरेटेड डिजिटल रसीद (प्रिंटर रेडी कॉपी)")
        
        # 🖨️ वन-क्लिक डायरेक्ट प्रिंटर कमांड बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 15px 30px; border: 2px solid black; border-radius: 5px; cursor: pointer; width: 100%; font-size: 18px;">🖨️ यहाँ क्लिक करके तुरंत रसीद प्रिंटर से बाहर निकालें</button>', unsafe_allow_html=True)
        st.write(" ")
        
        # साफ़ बिना एरर वाला इनफ़ो बॉक्स
        st.info("📄 रसीद ID: " + str(rb['bill_id']) + "  |  📅 तारीख: " + str(rb['date']))
        st.write("🏢 **प्रॉपर्टी का नाम:** " + str(rb['prop_name']) + " (" + str(rb['location']) + ")")
        st.write("👤 **ग्राहक का नाम:** " + str(rb['cust_name']) + "  |  📞 **मोबाइल:** " + str(rb['phone']))
        
        st.write("---")
        st.write("🔸 मूल सौदा राशि: ₹" + str(rb['base']))
        st.write("🔸 विशेष छूट (Discount): ₹" + str(rb['disc']))
        st.success("🔹 कुल फाइनल सौदा मूल्य: ₹" + str(rb['base'] - rb['disc']))
        st.write("🟩 प्राप्त एडवांस (बयाना राशि): ₹" + str(rb['adv']))
        st.error("🔴 कुल बकाया राशि (PENDING DUE): ₹" + str(rb['due']))
        st.write("---")
        st.caption("Verified by Maa Property Cloud 2026")

    # ==================== सुरक्षित बिल रिकॉर्ड रजिस्टर (एडिट और डिलीट ऑप्शन) ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल记录 रजिस्टर")
    st.write("यहाँ आपके सभी पुराने बिल सुरक्षित हैं। आप किसी भी बिल को कभी भी डिलीट या एडिट कर सकते हैं:")
    
    r_list = list(st.session_state.bill_records)
    if len(r_list) > 0:
        for r_idx, r_data in enumerate(r_list):
            col_rec_info, col_rec_edit, col_rec_del = st.columns([3, 1, 1])
            
            with col_rec_info:
                st.code("🆔 " + str(r_data['bill_id']) + " | 📅 " + str(r_data['date']) + " | 👤 " + str(r_data['cust_name']) + " | 🏢 " + str(r_data['prop_name']) + " | 🔴 बकाया: ₹" + str(r_data['due']))
            
            with col_rec_edit:
                if st.button("✏️ एडिट करें", key="edit_bill_id_" + str(r_idx)):
                    st.session_state.edit_index = r_idx
                    st.rerun()
                    
            with col_rec_del:
                if st.button("🗑️ डिलीट", key="del_bill_id_" + str(r_idx)):
                    st.session_state.bill_records.pop(r_idx)
                    st.session_state.active_bill = None
                    st.warning("🗑️ रसीद को रजिस्टर से डिलीट कर दिया गया है!")
                    st.rerun()
    else:
        st.write("अभी कोई रिकॉर्ड सुरक्षित नहीं है।")
