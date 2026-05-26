import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. पेज सेटअप और टाइटल
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# 2. पूरी तरह से सुरक्षित डेटाबेस लॉकिंग (Error Proof Structure)
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

# डिफ़ॉल्ट पुराना बिल रिकॉर्ड एकदम सही फॉर्मेट में ताकि KeyError कभी न आए
if 'bill_records' not in st.session_state:
    st.session_state.bill_records = [
        {
            "bill_id": "INV-3012", 
            "date": "26-05-2026", 
            "prop_name": "Maa Property", 
            "location": "Chatarkhar", 
            "cust_name": "Umasankar", 
            "phone": "8109471091", 
            "base": 20000000, 
            "disc": 0, 
            "adv": 100000, 
            "due": 19900000
        }
    ]

if 'active_bill' not in st.session_state:
    st.session_state.active_bill = None

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# मुख्य स्क्रीन हेडर
st.title("⚡ मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026")
st.write("---")

# तीन प्रोफेशनल मुख्य टैब
tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (Properties)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग एवं सुरक्षित रजिस्टर"])

# ==================== टैब 1: लाइव प्रॉपर्टीज स्क्रीन ====================
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("---")
    
    # एरर से बचने के लिए लिस्ट को सुरक्षित लूप में चलाना
    props_list = list(st.session_state.properties)
    for index, p in enumerate(props_list):
        col_info, col_del = st.columns([4, 1])
        with col_info:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{p['rate']}")
            st.write(f"👤 मालिक: {p['owner']}")
            
            # व्हाट्सएप लिंक जनरेटर
            msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} में इंटरेस्ट है।"
            wa_url = "https://wa.me/918109471091?text=" + msg.replace(" ", "%20")
            st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
            
        with col_del:
            st.write(" ")
            st.write(" ")
            if st.button("❌ प्रॉपर्टी हटाएँ", key=f"del_property_key_{index}"):
                st.session_state.properties.pop(index)
                st.warning("🗑️ प्रॉपर्टी हटा दी गई है!")
                st.rerun()
        st.write("---")

# ==================== टैब 2: नई प्रॉपर्टी एंट्री ====================
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("property_add_form_new", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        if st.form_submit_button("☁️ सुरक्षित लाइव सेव करें"):
            if n and r:
                new_id = "PROP-" + str(random.randint(400, 999))
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o
                })
                st.success("🎉 नई प्रॉपर्टी सफलतापूर्वक लाइव सुरक्षित कर दी गई है!")
                st.rerun()
            else:
                st.error("कृपया प्रॉपर्टी का नाम और कीमत भरना अनिवार्य है!")

# ==================== टैब 3: डिजिटल बिलिंग और सुरक्षित रिकॉर्ड रजिस्टर ====================
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    
    # चेक करें कि कोई रिकॉर्ड एडिट मोड में है या नहीं
    is_edit = st.session_state.edit_index is not None
    if is_edit:
        st.warning("⚠️ आप अभी रिकॉर्ड रजिस्टर में पुराने बिल को बदल (Edit) रहे हैं!")
        edit_data = st.session_state.bill_records[st.session_state.edit_index]
        default_bname = edit_data["prop_name"]
        default_bloc = edit_data["location"]
        default_cname = edit_data["cust_name"]
        default_cphone = edit_data["phone"]
        default_base = int(edit_data["base"])
        default_disc = int(edit_data["disc"])
        default_adv = int(edit_data["adv"])
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
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=default_base, step=1000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=default_disc, step=500)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=default_adv, step=1000)

    # रसीद की सटीक मैथ कैलकुलेशन
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    
    st.write(" ")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if is_edit:
            if st.button("💾 एडिट किया हुआ बिल अपडेट करें", type="primary"):
                idx = st.session_state.edit_index
                updated_record = {
                    "bill_id": edit_data["bill_id"], 
                    "date": edit_data["date"],
                    "prop_name": b_name, 
                    "location": b_loc, 
                    "cust_name": c_name, 
                    "phone": c_phone,
                    "base": base_price, 
                    "disc": disc, 
                    "adv": adv, 
                    "due": pending_amount
                }
                st.session_state.bill_records[idx] = updated_record
                st.session_state.active_bill = updated_record
                st.session_state.edit_index = None # एडिट समाप्त
                st.success("✅ रिकॉर्ड सफलतापूर्वक अपडेट (Edit) हो गया!")
                st.rerun()
        else:
            if st.button("✨ नई डिजिटल रसीद तैयार करें", type="primary"):
                if b_name == "":
                    st.error("कृपया प्रॉपर्टी का नाम लिखें!")
                else:
                    inv_id = "INV-" + str(random.randint(3000, 3999))
                    new_bill = {
                        "bill_id": inv_id, 
                        "date": current_date,
                        "prop_name": b_name, 
                        "location": b_loc, 
                        "cust_name": c_name, 
                        "phone": c_phone,
                        "base": base_price, 
                        "disc": disc, 
                        "adv": adv, 
                        "due": pending_amount
                    }
                    st.session_state.active_bill = new_bill
                    st.session_state.bill_records.append(new_bill)
                    st.success("✅ नई डिजिटल रसीद रजिस्टर में नीचे सुरक्षित हो चुकी है!")

    with col_btn2:
        if is_edit:
            if st.button("❌ बदलाव रद्द करें (Cancel)"):
                st.session_state.edit_index = None
                st.rerun()

    # ==================== रसीद का सुंदर डायरेक्ट प्रिंटर लेआउट बॉक्स ====================
    if st.session_state.active_bill:
        rb = st.session_state.active_bill
        st.write("---")
        st.write("### 🧾 जनरेटेड डिजिटल रसीद (प्रिंटर रेडी कॉपी)")
        
        # 🖨️ एक क्लिक पर बिना रुकावट प्रिंट करने वाला हाई-क्वालिटी बटन
        st.markdown('<button onclick="window.print()" style="background-color: #00ffcc; color: black; font-weight: bold; padding: 14px 30px; border: 2px solid #000; border-radius: 5px; cursor: pointer; width: 100%; font-size: 18px; margin-bottom: 15px;">🖨️ यहाँ क्लिक करके तुरंत रसीद प्रिंटर से बाहर निकालें</button>', unsafe_allow_html=True)
        
        # रसीद स्लिप डिज़ाइन बॉक्स
        st.info(f"📄 रसीद ID: {rb['bill_id']}  |  📅 तारीख: {rb['date']}")
        st.write(f"🏢 **प्रॉपर्टी का नाम:** {rb['prop_name']} ({rb['location']})")
        st.write(f"👤 **ग्राहक का नाम:** {rb['cust_name']}  |  📞 **मोबाइल:** {rb['phone']}")
        
        st.write("---")
        st.write(f"🔸 मूल सौदा राशि: ₹{rb['base']:,}")
        st.write(f"🔸 विशेष छूट (Discount): ₹{rb['disc']:,}")
        st.success(f"🔹 कुल फाइनल सौदा मूल्य: ₹{(rb['base'] - rb['disc']):,}")
        st.write(f"🟩 प्राप्त एडवांस (बयाना राशि): ₹{rb['adv']:,}")
        st.error(f"🔴 कुल बकाया राशि (PENDING DUE): ₹{rb['due']:,}")
        st.write("---")
        st.caption("Verified by Maa Property Cloud 2026")

    # ==================== पूरी तरह सुरक्षित बिल रिकॉर्ड रजिस्टर (बिना एरर वाला) ====================
    st.write("---")
    st.markdown("### 📁 सुरक्षित बिल रिकॉर्ड रजिस्टर")
    st.write("यहाँ आपके सभी पुराने बिल सुरक्षित हैं। आप किसी भी बिल को कभी भी डिलीट या एडिट कर सकते हैं:")
    
    # डेटाबेस को सुरक्षित रूप से लिस्ट में कन्वर्ट करके लूप चलाना ताकि डिलीट करने पर क्रैश न हो
    records_list = list(st.session_state.bill_records)
    if len(records_list) > 0:
        for r_idx, r_data in enumerate(records_list):
            col_rec_info, col_rec_edit, col_rec_del = st.columns([3, 1, 1])
            
            with col_rec_info:
                # बिना किसी एरर के सीधा और साफ़ स्ट्रिंग डिस्प्ले
                st.code(f"🆔 {r_data['bill_id']} | 📅 {r_data['date']} | 👤 {r_data['cust_name']} | 🏢 {r_data['prop_name']} | 🔴 बकाया: ₹{r_data['due']:,}")
            
            with col_rec_edit:
                if st.button("✏️ एडिट", key=f"btn_edit_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.edit_index = r_idx
                    st.rerun()
                    
            with col_rec_del:
                if st.button("🗑️ डिलीट", key=f"btn_del_rec_{r_data['bill_id']}_{r_idx}"):
                    st.session_state.bill_records.pop(r_idx)
                    # अगर एक्टिव रसीद डिलीट हुई है तो उसे स्क्रीन से हटाओ
                    if st.session_state.active_bill and st.session_state.active_bill["bill_id"] == r_data["bill_id"]:
                        st.session_state.active_bill = None
                    st.warning(f"🗑️ रसीद {r_data['bill_id']} को रजिस्टर से हमेशा के लिए हटा दिया गया है!")
                    st.rerun()
    else:
        st.write("अभी रजिस्टर में कोई बिल सुरक्षित नहीं है।")
